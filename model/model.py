from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO

        lista_tuple = list()
        for impianto in self._impianti:
            lista = list()
            consumi = impianto.get_consumi()
            for consumo in consumi:
                if mese == consumo.data.month:
                    lista.append(consumo.kwh)

            media_giornaliera = float(sum(lista) / len(lista))

            tupla = (impianto.nome, media_giornaliera)
            lista_tuple.append(tupla)

        return lista_tuple

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO

        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
                return
        else:
            for id_impianto in consumi_settimana.keys():
                costo_switch = 0
                if ultimo_impianto is not None and id_impianto != ultimo_impianto:
                    costo_switch = 5

                costo_variabile = consumi_settimana[id_impianto][giorno - 1]

                nuovo_costo_totale = costo_corrente + costo_switch + costo_variabile

                if self.__costo_ottimo == -1 or nuovo_costo_totale < self.__costo_ottimo:
                    sequenza_parziale.append(id_impianto)

                    self.__ricorsione(sequenza_parziale, giorno + 1, id_impianto, nuovo_costo_totale, consumi_settimana)

                    sequenza_parziale.pop()

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO

        diz = dict()
        impianti = self._impianti
        for impianto in impianti:
            consumi = impianto.get_consumi()
            diz[impianto.id] = [consumo.kwh for consumo in consumi if mese == consumo.data.month and 1 <= consumo.data.day <= 7]
                                    # List Comprehension
        return diz
