"""
AI Service for Chatbot - Integrates with OpenAI or other AI providers
"""
from app.core.config import settings
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.models.venta import Venta
from app.models.item_inventario import ItemInventario
from app.models.receta import Receta

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        
        if self.api_key:
            self.llm = ChatOpenAI(
                model_name=self.model,
                temperature=self.temperature,
                openai_api_key=self.api_key
            )
        else:
            self.llm = None
    
    def get_business_context(self, db: Session) -> Dict[str, Any]:
        """
        Extract real-time business context from the database
        """
        context = {}
        
        # 1. Ventas de Hoy
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        ventas_hoy = db.query(func.sum(Venta.total)).filter(
            Venta.fecha_creacion >= today_start,
            Venta.estado == "COMPLETADA"
        ).scalar() or 0.0
        
        count_hoy = db.query(func.count(Venta.id)).filter(
            Venta.fecha_creacion >= today_start,
            Venta.estado == "COMPLETADA"
        ).scalar() or 0
        
        context["sales"] = {
            "today": round(ventas_hoy, 2),
            "count_today": count_hoy
        }
        
        # 2. Inventario Crítico
        critical_items = db.query(ItemInventario).filter(
            ItemInventario.cantidad <= ItemInventario.stock_minimo
        ).limit(5).all()
        
        context["inventory"] = {
            "critical_items": [
                {
                    "name": item.nombre,
                    "quantity": item.cantidad,
                    "unit": item.unidad,
                    "min_stock": item.stock_minimo
                } for item in critical_items
            ]
        }
        
        # 3. Receta más rentable (Top 3)
        top_recipes = db.query(Receta).order_by(desc(Receta.margen)).limit(3).all()
        
        context["recipes"] = {
            "most_profitable": [
                {
                    "name": r.nombre,
                    "margin": round(r.margen, 2),
                    "cost": round(r.costo, 2),
                    "price": round(r.precio, 2)
                } for r in top_recipes
            ]
        }
        
        return context

    async def get_chat_response(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get AI response for chatbot message
        """
        if not self.llm:
            return self._get_fallback_response(message, context)
        
        # Build prompt with context
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{user_message}")
        ])
        
        # Format context for the prompt
        context_str = self._format_context(context) if context else "No hay datos disponibles en este momento."
        
        try:
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            response = await chain.arun(
                user_message=f"DATOS DEL NEGOCIO (Contexto Real):\n{context_str}\n\nPREGUNTA DEL USUARIO: {message}"
            )
            return response
        except Exception as e:
            print(f"Error calling AI service: {e}")
            return self._get_fallback_response(message, context)
    
    def _get_system_prompt(self) -> str:
        return """Eres 'ChefBot', el asistente inteligente de GastroSmart AI.
Tu misión es ayudar al dueño del restaurante con información estratégica basada en los datos reales que se te proporcionan.

Reglas:
1. Responde SIEMPRE basándote en el 'Contexto Real' proporcionado. No inventes números.
2. Si el contexto indica stocks bajos, sugiérele reabastecer esos productos específicos con urgencia.
3. Sé profesional pero amable, usa emojis culinarios (🥩, 🥗, 💰) ocasionalmente.
4. Si te preguntan algo que no está en los datos, di amablemente que no tienes esa información por ahora.
5. Responde siempre en español.
"""
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format business context for the AI prompt"""
        lines = []
        
        # Sales
        if "sales" in context:
            s = context["sales"]
            lines.append(f"--- VENTAS DE HOY ({datetime.now().strftime('%d/%m/%Y')}) ---")
            lines.append(f"Total Vendido: Bs. {s.get('today', 0)}")
            lines.append(f"Cantidad de Pedidos: {s.get('count_today', 0)}")
        
        # Inventory
        if "inventory" in context and context["inventory"].get("critical_items"):
            lines.append("\n--- ALERTAS DE INVENTARIO (Bajo Stock) ---")
            for item in context["inventory"]["critical_items"]:
                lines.append(f"⚠️ {item['name']}: Quedan {item['quantity']} {item['unit']} (Mínimo requerido: {item['min_stock']})")
        
        # Recipes
        if "recipes" in context and context["recipes"].get("most_profitable"):
            lines.append("\n--- PLATOS MÁS RENTABLES ---")
            for r in context["recipes"]["most_profitable"]:
                lines.append(f"🏆 {r['name']}: Margen {r['margin']}% (Costo: {r['cost']} -> Precio: {r['price']})")
                
        return "\n".join(lines)
    
    def _get_fallback_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Simple rules engine when OpenAI is not configured"""
        msg = message.lower()
        
        # Logic for sales
        if "venta" in msg or "gan" in msg: # ganancia, gané
            if context and "sales" in context:
                s = context["sales"]
                return f"Hoy llevamos {s['count_today']} ventas por un total de Bs. {s['today']}. 💰"
            return "No tengo datos de ventas en este momento."
            
        # Logic for inventory
        if "stock" in msg or "falta" in msg or "comprar" in msg:
            if context and "inventory" in context:
                crit = context["inventory"].get("critical_items", [])
                if crit:
                    items = ", ".join([f"{i['name']} ({i['quantity']}{i['unit']})" for i in crit])
                    return f"⚠️ Atención: Tienes {len(crit)} productos con stock bajo: {items}."
                return "✅ Todo el inventario parece estar en orden por encima del stock mínimo."
        
        # Logic for recipes
        if "plato" in msg or "rentable" in msg or "mejor" in msg:
            if context and "recipes" in context:
                top = context["recipes"].get("most_profitable", [])
                if top:
                    r = top[0]
                    return f"Tu plato estrella por margen es: {r['name']} ({r['margin']}% de rentabilidad). 🏆"
        
        return "Soy ChefBot. Configura tu API Key de OpenAI para que pueda responderte cualquier pregunta. Por ahora solo puedo darte datos básicos de ventas e inventario si me preguntas directamente. 🤖"

# Singleton
ai_service = AIService()


