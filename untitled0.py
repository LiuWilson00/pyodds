import matplotlib.pyplot as plt
pd.options.display.mpl_style = 'default'
ts = Series(randn(1000), index=date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()