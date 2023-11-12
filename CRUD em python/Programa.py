import tkinter as tk
from tkinter import ttk
import psycopg2
from datetime import datetime, timedelta
import crud as crud
from registro_gui import RegistroGUI

class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()

        self.lbRaca = tk.Label(win, text='Raça do Pet:')
        self.lblNome = tk.Label(win, text='Nome do Pet')
        self.lblPeso = tk.Label(win, text='Peso do Pet')
        self.lblDataConsulta = tk.Label(win, text='Data da Consulta: (AAAA/MM/DD)')
        self.lblValorMedicamentos = tk.Label(win, text='Valor dos Medicamentos')
        self.lbValorTotal = tk.Label(win, text='Valor Total:')

        self.txtRaca = tk.Entry(bd=2, width=30)
        self.txtNome = tk.Entry(bd=2, width=30)
        self.txtPeso = tk.Entry(bd=2, width=30)
        self.txtDataConsulta = tk.Entry(win, bd=2, width=30)
        self.txtValorMedicamentos = tk.Entry(bd=2, width=30)

        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarPet)
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.fAtualizarPet)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.fExcluirPet)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)
        self.btnCalcularProximaConsulta = tk.Button(win, text='Calcular Próxima Consulta', command=self.calcularProximaConsulta)

        titulo_label = tk.Label(win, text='Cadastro de Pets', font=("Helvetica", 16))
        titulo_label.pack(pady=5)
        
        self.lbRaca.pack(pady=5)
        self.txtRaca.pack(pady=0)

        self.lblNome.pack(pady=5)
        self.txtNome.pack(pady=0)

        self.lblPeso.pack(pady=5)
        self.txtPeso.pack(pady=0)

        self.lblDataConsulta.pack(pady=5)
        self.txtDataConsulta.pack(pady=0)

        self.lblValorMedicamentos.pack(pady=5)
        self.txtValorMedicamentos.pack(pady=0)

        

        self.btnCadastrar.place(x=140, y=402)
        self.btnAtualizar.place(x=240, y=402)
        self.btnExcluir.place(x=340, y=402)
        self.btnLimpar.place(x=440, y=402)
        self.btnCalcularProximaConsulta.pack(pady=3)


        self.txtRaca.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.txtNome.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.txtPeso.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.txtDataConsulta.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)

        self.lbProximaConsulta = tk.Label(win, text='Próxima Consulta:')
        self.lbProximaConsulta.pack(pady=3)
        self.lbValorTotal.pack(pady=5)

    def atualizarValorTotal(self):
        try:
            valor_medicamentos = float(self.txtValorMedicamentos.get())
            valor_consulta = 80
            valor_total = valor_consulta + valor_medicamentos + (valor_consulta * 0.10)
            self.lbValorTotal.config(text=f'Valor Total: R${valor_total:.2f}')
        except ValueError:
            print('O valor do medicamento deve ser um número.')
        
    def calcularProximaConsulta(self):
        try:
            raca, nome, peso, data_consulta, valor_medicamentos = self.fLerCampos()
            data_consulta_original = data_consulta  
            data_consulta_formatada = self.formatarData(data_consulta)

            if data_consulta_formatada:
                data_consulta = datetime.strptime(data_consulta_formatada, '%Y%m%d')
                dias_para_proxima_consulta = 7
                data_proxima_consulta = data_consulta + timedelta(days=dias_para_proxima_consulta)
                data_proxima_consulta_str = data_proxima_consulta.strftime('%d/%m/%Y')

                self.lbProximaConsulta.config(text=f'Próxima Consulta: {data_proxima_consulta_str}')

                print('Próxima consulta calculada com sucesso!')
                return data_consulta_original  
        except Exception as e:
            print('Não foi possível calcular a próxima consulta. Erro:', e)
        return None

    def formatarData(self, data_consulta):
    
        if len(data_consulta) == 8 and data_consulta.isdigit():
            return data_consulta
        else:
            print('Formato de data inválido. Use AAAAMMDD.')
            return None

    def fLerCampos(self):
        try:
            raca = self.txtRaca.get()
            nome = self.txtNome.get()
            peso = float(self.txtPeso.get()) if self.txtPeso.get() else 0.0
            data_consulta = self.txtDataConsulta.get()
            valor_medicamentos = float(self.txtValorMedicamentos.get()) if self.txtValorMedicamentos.get() else 0.0
            self.atualizarValorTotal()
            print('Leitura dos Dados com Sucesso!')
            return raca, nome, peso, data_consulta, valor_medicamentos
        except ValueError:
            print('Não foi possível ler os dados. Certifique-se de que os campos numéricos estão preenchidos corretamente.')
            return None, None, None, None, None

    def fCadastrarPet(self):
        try:
            raca, nome, peso, data_consulta, valor_medicamentos = self.fLerCampos()
            data_consulta_original = self.calcularProximaConsulta()  

            if data_consulta_original:
                valor_consulta = 80
                valor_total = valor_consulta + valor_medicamentos + (valor_consulta * 0.10)
                
                self.objBD.inserirDados(raca, nome, peso, data_consulta_original, valor_medicamentos, valor_total)
                self.fLimparTela()
                print('Pet Cadastrado com Sucesso!')
        except Exception as e:
            print('Não foi possível fazer o cadastro. Erro:', e)


    def fLimparTela(self):
        try:
            self.txtRaca.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPeso.delete(0, tk.END)
            self.txtDataConsulta.delete(0, tk.END)
            self.lbProximaConsulta.config(text='Próxima Consulta:')
            self.txtValorMedicamentos.delete(0, tk.END)
            self.lbValorTotal.config(text='Valor Total: ')
            
            print('Campos Limpos!')
        except:
            print('Não foi possível limpar os campos.')

    def fAtualizarPet(self):
        try:
            raca, nome, peso, data_consulta, valor_medicamentos = self.fLerCampos()
            data_consulta = self.formatarData(data_consulta)
            proxima_consulta = self.txtDataConsulta.get()

            if raca and nome and peso and data_consulta and proxima_consulta:
                valor_consulta = 80
                valor_total = valor_consulta + valor_medicamentos + (valor_consulta * 0.10)
                self.objBD.atualizarDados(raca, nome, peso, data_consulta, proxima_consulta, valor_medicamentos, valor_total)
                self.lbValorTotal.config(text=f'Valor Total: R${valor_total:.2f}')
                self.fLimparTela()
                print('Pet Atualizado com Sucesso!')
        except:
            print('Não foi possível fazer a atualização.')

    def fExcluirPet(self):
        try:
            raca, nome, peso, data_consulta, valor_medicamentos = self.fLerCampos()
            if raca and nome and peso is not None:  # Certifique-se de que os campos obrigatórios estão preenchidos
                self.objBD.excluirDados(raca, nome, peso)
                self.fLimparTela()
                print('Pet Excluído com Sucesso!')
            else:
                print('Campos obrigatórios não preenchidos para a exclusão.')
        except Exception as e:
            print('Não foi possível fazer a exclusão do Pet. Erro:', e)

    def mostrarRegistros(self):
        
        registro_gui = RegistroGUI(tk.Toplevel())

# Programa Principal
janela = tk.Tk()
Principal = PrincipalBD(janela)
janela.title('Bem Vindo à Tela de Cadastro de Pets')
janela.geometry("600x500")

btn_mostrar_registros = tk.Button(janela, text='Mostrar Registros', command=Principal.mostrarRegistros)
btn_mostrar_registros.pack(pady=38)

janela.mainloop()