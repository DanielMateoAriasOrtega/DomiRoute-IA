# Base de conocimiento de DomiRoute IA

GRAFO = {
    "Restaurante": ["Calle 1"],
    "Calle 1": ["Restaurante", "Calle 2", "Calle 3"],
    "Calle 2": ["Calle 1", "Calle 4"],
    "Calle 3": ["Calle 1", "Calle 5"],
    "Calle 4": ["Calle 2", "Cliente"],
    "Calle 5": ["Calle 3", "Cliente"],
    "Cliente": ["Calle 4", "Calle 5"]
}