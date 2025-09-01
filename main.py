import random
from dataclasses import dataclass
import time
#Classes de dados
@dataclass 
class DadosViagem:
    origem: str
    destino: str
    data_ida: str
    data_volta: str
    precisa_hotel: bool
    precisa_carro: bool

@dataclass
class ResultadoReserva:
    sucesso: bool = False
    mensagem: str = ""
    codigo_voo: str = ""
    codigo_hotel: str = ""
    codigo_carro: str = ""
    preco_total: float = 0.0



#SUBSISTEMAS

class SistemaVoos:
    def verificar_disponibilidade(self, origem: str, destino: str, data_ida: str, data_volta: str) -> bool:
        print(f"Verificando disponibilidade de voos de {origem} para {destino} em {data_ida} até {data_volta}")
        return random.random() > 0.1  # 90% de chance de sucesso
    def reservar_voo(self, origem: str, destino: str, data_ida: str, data_volta: str) -> str:
        print(f"Reservando voo: de {origem} para {destino} em {data_ida} até {data_volta}")
        return f"VOO{random.randint(1000,9999)}"
    
    def calcular_preco_voo(self, origem: str, destino: str) -> float:
        print(f"💰 Calculando preço do voo para o trecho {origem} - {destino}")
        return 300.0 + random.random() * 500  # Preço entre 300-800

class SistemaHoteis:
    def verificar_disponibilidade_quarto(self, destino: str, check_in: str, check_out: str) -> bool:
        print(f"Verificando disponibilidade de hotéis em {destino} de {check_in} até {check_out}")
        return random.random() > 0.15  # 85% de chance de sucesso
    
    def reservar_quarto(self, destino: str, check_in: str, check_out: str) -> str:
        print(f"Reservando quarto em {destino} de {check_in} até {check_out}")
        time.sleep(1)
        return f"HOTEL{random.randint(1000,9999)}"
    
    def calcular_preco_hotel(self, destino: str, numero_dias: int) -> float:
        print(f"💰 Calculando preço do hotel em {destino} para {numero_dias} dias")
        return 200.0 * numero_dias + random.random() * 300  # Preço entre 200-500 por dia

class SistemaAluguelCarros:

    def verificar_disponibilidade(self, destino: str, data_retirada: str, data_devolucao: str) -> bool:
        print(f"Verificando disponibilidade de carros em {destino} de {data_retirada} até {data_devolucao}")
        return random.random() > 0.2  # 80% de chance de sucesso

    def alugar_carro(self, destino: str, data_retirada: str, data_devolucao: str) -> str:
        print(f"Alugando carro em {destino} de {data_retirada} até {data_devolucao}")
        time.sleep(1)
        print("Carro alugado com sucesso.")
        return f"Código do carro: {random.randint(1000,9999)}"
    def calcular_preco_aluguel(self, destino: str, data_retirada: str, data_devolucao: str) -> float:
        print(f"💰 Calculando preço do aluguel de carro em {destino} de {data_retirada} até {data_devolucao}")
        return 100.0 + random.random() * 200  # Preço entre 100-300

class SistemaPagamentos:
    def processar_pagamento(self, valor: float) -> bool:
        print(f"Processando pagamento de R${valor:.2f}")
        time.sleep(1)
        return random.random() > 0.05 #95% de chance de sucesso

#FACADE

class ReservaViagemFacade:
    def __init__(self):
        self.sistema_voos = SistemaVoos()
        self.sistema_hoteis = SistemaHoteis()
        self.sistema_aluguel_carros = SistemaAluguelCarros()
        self.sistema_pagamentos = SistemaPagamentos()
    
    def reservar_viagem_completa(self, dados: DadosViagem) -> ResultadoReserva:
        print("Iniciando reserva de viagem completa...")
        resultado = ResultadoReserva()
        preco_total = 0.0

        try:
            # 1. Verificar e reservar voo
            if not self.sistema_voos.verificar_disponibilidade(dados.origem, dados.destino, dados.data_ida, dados.data_volta):
                resultado.mensagem = "Não há voos disponíveis."
                return resultado
            resultado.codigo_voo = self.sistema_voos.reservar_voo(dados.origem, dados.destino, dados.data_ida, dados.data_volta)
            preco_total += self.sistema_voos.calcular_preco_voo(dados.origem, dados.destino)

            # 2. Verificar e reservar hotel (se o cliente precisar)
            if dados.precisa_hotel:
                if not self.sistema_hoteis.verificar_disponibilidade_quarto(dados.destino, dados.data_ida, dados.data_volta):
                    resultado.mensagem = "Não há quartos de hotel disponíveis paras as datas informadas."
                    return resultado
                resultado.codigo_hotel = self.sistema_hoteis.reservar_quarto(dados.destino, dados.data_ida, dados.data_volta)
                dias_estadia = self.calcular_dias_estadia(dados.data_ida, dados.data_volta)
                preco_total += self.sistema_hoteis.calcular_preco_hotel(dados.destino, dias_estadia)

            # 3. Verificar e alugar carro (se o cliente precisar)
            if dados.precisa_carro:
                if not self.sistema_aluguel_carros.verificar_disponibilidade(dados.destino, dados.data_ida, dados.data_volta):
                    resultado.mensagem = "Não há carros disponíveis para aluguel nas datas informadas."
                    return resultado
                resultado.codigo_carro = self.sistema_aluguel_carros.alugar_carro(dados.destino, dados.data_ida, dados.data_volta)
                dias_aluguel = self.calcular_dias_estadia(dados.data_ida, dados.data_volta)
                preco_total += self.sistema_aluguel_carros.calcular_preco_aluguel(dados.destino, dados.data_ida, dados.data_volta)

            # 4. Processar pagamento
            print("Processando o pagamento total")
            if not self.sistema_pagamentos.processar_pagamento(preco_total):
                resultado.mensagem = "Falha no processamento do pagamento."
                return resultado

            print("=" * 50)
            print("🎉 RESERVA CONCLUÍDA COM SUCESSO! 🎉")
            resultado.sucesso = True
            resultado.preco_total = preco_total
        except Exception as e:
            resultado.mensagem = f"❌ Erro inesperado durante a reserva: {str(e)}"

        return resultado

    def obter_orcamento_viagem(self,dados: DadosViagem) -> float:
        print("Calculando orçamento da viagem")
        orcamento = 0.0

        # 1. Calcular preço do voo
        if self.sistema_voos.verificar_disponibilidade(dados.origem, dados.destino, dados.data_ida, dados.data_volta):
            preco_voo = self.sistema_voos.calcular_preco_voo(dados.origem, dados.destino)
            orcamento += preco_voo
            print(f"Voo: R${preco_voo:.2f}")
        # 2. Calcular preço do hotel (se necessário)
        if dados.precisa_hotel:
            if self.sistema_hoteis.verificar_disponibilidade_quarto(dados.destino, dados.data_ida, dados.data_volta):
                dias_estadia = self.calcular_dias_estadia(dados.data_ida, dados.data_volta)
                preco_hotel = self.sistema_hoteis.calcular_preco_hotel(dados.destino, dias_estadia)
                orcamento += preco_hotel
                print(f"Hotel ({dias_estadia} dias): R${preco_hotel:.2f}")

        # 3. Calcular preço do aluguel de carro (se necessário)
        if dados.precisa_carro:
            if self.sistema_aluguel_carros.verificar_disponibilidade(dados.destino, dados.data_ida, dados.data_volta):
                dias_aluguel = self.calcular_dias_estadia(dados.data_ida, dados.data_volta)
                preco_carro = self.sistema_aluguel_carros.calcular_preco_aluguel(dados.destino, dados.data_ida, dados.data_volta)
                orcamento += preco_carro
                print(f"Carro ({dias_aluguel} dias): R${preco_carro:.2f}")

        print(f"Orçamento total da viagem: R${orcamento:.2f}")
        return orcamento
    def calcular_dias_estadia(self, data_ida: str, data_volta: str) -> int:
        # Simulação de 5 dias de estadia
        return 5
    
#Teste do cliente no sistema

class Cliente:
    def __init__(self, nome: str):
        self.nome = nome
        self.facade = ReservaViagemFacade()
        self.facade_reserva = self.facade
    
    def solicitar_reserva_completa(self):
        print(f"Cliente: {self.nome}")
        print("Solicitando reserva de viagem completa...")

        #Situação 1: Viagem completa
        viagem_completa = DadosViagem(
            origem="Rio de Janeiro",
            destino="Miami",
            data_ida="2024-12-20",
            data_volta="2024-12-27",
            precisa_hotel=True,
            precisa_carro=True
        )

        #Orçamento
        orcamento = self.facade.obter_orcamento_viagem(viagem_completa)
        print(f"Orçamento total da viagem: R${orcamento:.2f}")

        #Reserva
        resultado1 = self.facade_reserva.reservar_viagem_completa(viagem_completa)
        self._exibir_resultado(resultado1)

        # Situação 2: Somente voo
        viagem_voo = DadosViagem(
            origem="Miami",
            destino="Rio de Janeiro",
            data_ida="2024-12-20",
            data_volta="2024-12-27",
            precisa_hotel=False,
            precisa_carro=False
        )

        # Orçamento
        orcamento = self.facade.obter_orcamento_viagem(viagem_voo)
        print(f"Orçamento total da viagem: R${orcamento:.2f}")

        # Reserva
        resultado2 = self.facade.reservar_viagem_completa(viagem_voo)
        self._exibir_resultado(resultado2)
    
    def solicitar_orcamento(self):
        #Situação 3 - Apenas Orçamento
        print(f"Cliente: {self.nome}")
        print("Solicitando orçamento de viagem...")

        viagem_orcamento = DadosViagem(
            origem="Rio de Janeiro",
            destino="Tóquio",
            data_ida="2024-12-20",
            data_volta="2024-12-27",
            precisa_hotel=False,
            precisa_carro=False
        )
           # Orçamento
        orcamento = self.facade.obter_orcamento_viagem(viagem_orcamento)
        print(f"Orçamento total da viagem: R${orcamento:.2f}")
    
    def _exibir_resultado(self, resultado: ResultadoReserva):
        print("\n📋 RESULTADO DA RESERVA:")
        print(f"Status: {'✅ SUCESSO' if resultado.sucesso else '❌ FALHA'}")
        if resultado.sucesso:
            print("Detalhes da reserva:")
            if resultado.codigo_voo:
                print(f"  ✈️ Código do voo: {resultado.codigo_voo}")
            if resultado.codigo_hotel:
                print(f"  🏨 Código do hotel: {resultado.codigo_hotel}")
            if resultado.codigo_carro:
                print(f"  🚗 Código do carro: {resultado.codigo_carro}")
            print(f"  💰 Preço total: R$ {resultado.preco_total:.2f}")

#Executando o sistema
def main():
    #Criando o cliente
    cliente1 = Cliente("Davi")
    #Teste 1: Reservas Completas
    cliente1.solicitar_reserva_completa()
    #Teste 2: Somente Orçamento
    cliente1.solicitar_orcamento()

if __name__ == "__main__":
    main()
