import os
import json
from pathlib import Path

def restore_setup_data(data_dir: Path):
	os.makedirs(data_dir, exist_ok=True)

	menu = [
		{
			"id": 1,
			"nome": "Café expresso",
			"agua": 40,
			"cafe": 8,
			"leite": 0,
			"chocolate": 0,
			"preparo": 5,
			"preco": 4.00,
		},
		{
			"id": 2,
			"nome": "Café longo",
			"agua": 120,
			"cafe": 8,
			"leite": 0,
			"chocolate": 0,
			"preparo": 8,
			"preco": 4.50,
		},
		{
			"id": 3,
			"nome": "Café com leite",
			"agua": 40,
			"cafe": 8,
			"leite": 150,
			"chocolate": 0,
			"preparo": 10,
			"preco": 6.00,
		},
		{
			"id": 4,
			"nome": "Cappuccino",
			"agua": 40,
			"cafe": 8,
			"leite": 100,
			"chocolate": 5,
			"preparo": 12,
			"preco": 6.50,
		},
		{
			"id": 5,
			"nome": "Chocolate quente",
			"agua": 50,
			"cafe": 0,
			"leite": 120,
			"chocolate": 30,
			"preparo": 12,
			"preco": 7.00,
		},
	]

	stock = {
		"agua": {"atual": 2000, "capacidade": 2000, "nivel_baixo": 400},
		"cafe": {"atual": 500, "capacidade": 500, "nivel_baixo": 100},
		"leite": {"atual": 1000, "capacidade": 1000, "nivel_baixo": 200},
		"chocolate": {"atual": 400, "capacidade": 400, "nivel_baixo": 80},
		"acucar": {"atual": 300, "capacidade": 300, "nivel_baixo": 60},
		"copos": {"atual": 50, "capacidade": 50, "nivel_baixo": 10},
	}

	state = {
		"estado": "PRONTA",  # PRONTA, PREPARANDO, AGUARDANDO_LIMPEZA, MANUTENCAO
		"credito": 0.00,
		"contador_limpeza": 0,
		"previsao_termino": None,
	}

	orders = []

	files = {
		"menu.json": menu,
		"stock.json": stock,
		"state.json": state,
		"orders.json": orders,
	}

	for file_name, file_content in files.items():
		path = os.path.join(data_dir, file_name)
		with open(path, "w", encoding="utf-8") as f:
			json.dump(file_content, f, ensure_ascii=False, indent=4)

	print("[INFO] Ambiente de dados inicializado com sucesso em app/data/!")


if __name__ == "__main__":
	DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
	restore_setup_data(DATA_DIR)