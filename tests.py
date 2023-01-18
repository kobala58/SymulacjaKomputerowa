import numpy as np

if __name__ == "__main__":
    data = sorted([(abs(x)).__round__(1) for x in np.random.normal(1, 0.5, 20)],reverse=True)
    wind_data = [data[0]]
    for idx,elem in enumerate(data):
        if idx == 0:
            continue
        elif idx%2 == 0:
            wind_data = [elem, *wind_data]
        else:
            wind_data.append(elem)
    return wind_data
