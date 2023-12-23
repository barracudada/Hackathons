import numpy as np

class MeanReversion:
    def __init__(self, window_size, fees):
        self.window_size = window_size
        self.fees = fees
        self.prev_prices = []

    def get_update(self, update):
        # по хорошему тот должен быть isinstance(update, CandleUpdate)
        if update['price'] is None:
            return 0
        
        price = update['price']
        if len(self.prev_prices) < self.window_size:
            self.prev_prices.append(price)
            return 0
        else:
            self.prev_prices.append(price)
            self.prev_prices.pop(0)
            if price < np.mean(self.prev_prices) * (1 + self.fees): #  
                return 1
            elif price > np.mean(self.prev_prices) * (1 - self.fees):
                return 1
            else:
                return 0


class MdUpdate:
    # Отвечает за виды того что к нам приходит в потоке данных
    def __init__(self):
        pass

class CandleUpdate(MdUpdate):
    def __init__(self, open, close, high, low, volume, ts):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.ts = ts

class NewsUpdate(MdUpdate):
    def __init__(self, text, ts):
        self.text = text
        self.ts = ts
...

class DataFlow:
    # Отвечает за поток данных (данные отсортирваны по времени)
    def __init__(self, local_ts, data):
        
        assert len(local_ts) == len(data), "Length of local_ts and data must be equal."
        self.local_ts = local_ts
        self.data = data
        self._index = 0
    
class CandleDataFlow(DataFlow):
    def __init__(self, local_ts, data):
        super().__init__(local_ts, data)
        self._index = 0
    
    def get_update(self):
        if self._index >= len(self.local_ts):
            return None
        else:
            update = CandleUpdate(
                self.data['open'][self._index],
                self.data['close'][self._index],
                self.data['high'][self._index],
                self.data['low'][self._index],
                self.data['volume'][self._index],
                self.local_ts[self._index]
            )
            self._index += 1
            return update
        
class NewsDataFlow(DataFlow):
    ...

class CombinatedDataFlow:
    # Отвечает за комбинацию потоков данных + сортируют данные по времени
    def __init__(self, data_flows):
        self.data_flows = data_flows
        self._index = 0
        self._current_ts = None
        self._current_update = None

    def get_update(self):
        ...

class Backtest:
    def __init__(self, data_flow, strategy):
        self.data_flow = data_flow
        self.strategy = strategy
        self._index = 0
        self._current_ts = None
        self._current_update = None

    def run(self):
        for i in self.data_flow:
            delta_position = self.strategy.get_update(i)
            ...
            