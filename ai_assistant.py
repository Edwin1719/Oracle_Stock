import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import repository

# Cargar variables de entorno (API Key)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Definición de las herramientas (funciones) que el asistente puede usar
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_inventory_stats",
            "description": "Obtiene estadísticas generales (valor total, alertas, resumen por categorías).",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "Obtiene la lista completa de TODOS los productos con sus detalles. Úsalo para encontrar el producto con más stock, el más caro, o hacer conteos detallados.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_stock_products",
            "description": "Lista los productos que están por debajo de su stock mínimo configurado.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Busca productos específicos por nombre o categoría.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {"type": "string", "description": "Término de búsqueda"},
                    "category": {"type": "string", "description": "Categoría opcional"}
                },
                "required": ["search_term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_movement_stats",
            "description": "Obtiene estadísticas de los movimientos (entradas y salidas).",
        }
    }
]

def call_function(name, args):
    """Mapea el nombre de la función de OpenAI a la función real en repository.py"""
    if name == "get_inventory_stats":
        return repository.get_inventory_stats()
    elif name == "list_products":
        return repository.list_products()
    elif name == "get_low_stock_products":
        return repository.get_low_stock_products()
    elif name == "search_products":
        return repository.search_products(args.get("search_term"), args.get("category"))
    elif name == "get_movement_stats":
        return repository.get_movement_stats()
    return None

def get_ai_response(messages):
    """Procesa la conversación con OpenAI y maneja las llamadas a funciones."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ Error: No se encontró la API Key en el archivo .env."

    try:
        # Primera llamada al modelo
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Si el modelo quiere usar herramientas
        if tool_calls:
            # Convertir el objeto de mensaje a un diccionario antes de añadirlo al historial
            assistant_msg_dict = {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in tool_calls
                ]
            }
            messages.append(assistant_msg_dict)
            
            # Ejecutar cada llamada a función
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                function_response = call_function(function_name, function_args)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })
            
            # Segunda llamada con los datos de la herramienta
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return second_response.choices[0].message.content
        
        return response_message.content

    except Exception as e:
        return f"❌ Error en el asistente: {str(e)}"
