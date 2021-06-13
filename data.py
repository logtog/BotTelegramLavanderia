import time
import datetime as dt


class Data:
    @staticmethod
    def dia_reserva():
        data_atual = time.localtime()
        date_string = time.strftime('%Y/%m/%d', data_atual)
        return data_atual.tm_mday, data_atual.tm_wday

    @staticmethod
    def soma_reserva(dia_semana, hoje):
        dia1, dia2 = None, None
        if dia_semana == 0:    # segunda
            dia1 = hoje + 1
            dia2 = hoje + 2
        elif dia_semana == 1:  # terça
            dia1 = hoje + 1
            dia2 = hoje + 2
        elif dia_semana == 2:  # quarta
            dia1 = hoje + 1
            dia2 = hoje + 2
        elif dia_semana == 3:  # quinta
            dia1 = hoje + 1
            dia2 = hoje + 2
        elif dia_semana == 4:  # sexta
            dia1 = hoje + 3
            dia2 = hoje + 4
        elif dia_semana == 5:  # sabado
            dia1 = hoje + 2
            dia2 = hoje + 3
        elif dia_semana == 6:  # domingo
            dia1 = hoje + 1
            dia2 = hoje + 2
        return dia1, dia2

    @staticmethod
    def verifica_digitado(digitado, dia1, dia2):
        digitado = int(digitado)
        dia1 = int(dia1)
        dia2 = int(dia2)
        if (digitado == dia1) or (digitado == dia2):
            return True
        else:
            return False

    @staticmethod
    def datetime():
        hoje = time.localtime()
        hoje = time.strftime("%Y/%m/%d %H:%M:%S", hoje)
        hoje = dt.datetime.strptime(hoje, '%Y/%m/%d %H:%M:%S')
        return hoje

    @staticmethod
    def troca_forma(i):
        date_string = dt.datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S')
        return date_string.strftime('%d/%m/%Y %H:%M:%S')
