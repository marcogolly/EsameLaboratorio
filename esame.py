#classe per le eccezioni
class ExamException(Exception):
  pass

class CSVTimeSeriesFile:
  #costruttore, con controllo sul nome del file
  def __init__(self, name =""):
    try:
      assert(isinstance(name, str))
      assert(name != "")
      self.name = name
    except:
      raise ExamException("name not valid")

  #metodo che restituisce la lista di dati
  def get_data(self):
    try:
      file = open(self.name, "r")
    except:
      raise ExamException ("cannot open the file")
    
    time_series=[]
    #nel file CSV ogni riga è scritta in questo modo: "timestamp, valore numerico"

    for line in file:
      try:
        tmp = line.split(",")
        assert(len(tmp) ==2)
        timestamp = int(tmp[0])
        temperature = float(tmp[1])
        assert(timestamp >=0) #controllo forse superfluo, verifico che i timestamps siano più recenti del 1970
        time_series.append([timestamp, temperature])
      except:
        print('the line "{}" is not valid'.format(line))
    file.close()

    #controllo i timestamp: verifico che siano ordinati e non ci siano doppioni
    for i in range(1, len(time_series)):
      if time_series[i-1][0]>=time_series[i][0]:
        raise ExamException("timestamps are not valid")
    
    #controllo che il file non sia vuoto o privo di dati utili
    try:
      assert(len(time_series)!=0)
    except:
      raise ExamException("file contains no time series")
      
    return time_series

def daily_stats(time_series):
  #qui inserisco le epochs dei giorni (alle 00:00)
  days_epoch =[]
  #qui inserisco le temperature, divise per giorno
  days_temperature =[]

  for data in time_series:
    day_start_epoch = data[0] - (data[0] % 86400)
    if day_start_epoch not in days_epoch: #se è il primo valore del giorno
      days_epoch.append(day_start_epoch)
      days_temperature.append([])
    #qui aggiungo la temperatura nella lista del giorno day_start_epoch a sua volta contenuta in days_temperature
    days_temperature[days_epoch.index(day_start_epoch)].append(data[1])

  days_result =[]
  for day_temperature in days_temperature:
    days_result.append([min(day_temperature), max(day_temperature), sum(day_temperature)/len(day_temperature)])

  return days_result