from project import trading_signal

def test_bullish_signal():
    assert trading_signal(221.055, 221.046, 220.986) == 1 #Here, 1 indicates Bullish Signal
    assert trading_signal(225.467, 225.460, 225.459) == 1
    assert trading_signal(223.289, 223.287, 223.270) == 1

def test_bearish_signal():
    assert trading_signal(221.954, 221.955, 221.972) == 0 #Here, 0 indicates Bearish Signal
    assert trading_signal(218.890, 218.903, 218.912) == 0
    assert trading_signal(223.422, 223.427, 223.431) == 0

def test_no_signal():
    assert trading_signal(220.057,221.221,220.050) == -1 #Here, -1 indicates No signal
    assert trading_signal(228.230,228.653,228.260) == -1

