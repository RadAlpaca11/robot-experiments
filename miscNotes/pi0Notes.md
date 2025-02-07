Seems like it is meant for bigger tasks.

Mentions that diverse data trained models are better than niche trained models.
First train on diverse data, then fine tune on niche data.

Model is also pre-trained on the internet, unlike openVLA, so it could probably recognize taylor swift.

The github repo is from an individual who used the paper to create the model.

ERROR: Package 'open-pi-zero' requires a different Python: 3.12.2 not in '==3.10.*'

also needed to change tensorflow to not specify a version




# Official model
* some paths needed to be changed:
```python
# from
import openpi
# to
import src.openpi

# from
import lerobot
# to
import lerobot0.lerobot1
```

# Legit version
```
# output
[[ 0.13390535  0.01700424 -0.21063898  0.01644268  0.05704939 -0.02811454
  -0.00322509 -0.00596324]
 [ 0.12645799  0.01811409 -0.20128379  0.01644268  0.01304735 -0.01439778
   0.00243884 -0.00596324]
 [ 0.13966098  0.01232559 -0.19209506  0.01644268  0.01363006 -0.00092508
   0.00977213 -0.00596324]
 [ 0.1577004  -0.00425252 -0.19317629  0.01644268  0.02401032 -0.00251041
   0.01249072 -0.00596324]
 [ 0.14583323 -0.01952565 -0.20515884  0.01644268  0.02248996 -0.02007945
   0.00476223 -0.00596324]
 [ 0.13624481 -0.00741766 -0.21705541  0.01644268  0.06200396 -0.03752242
  -0.01609694 -0.00596324]
 [ 0.18410508  0.05413977 -0.21451403  0.01644268  0.04302059 -0.0337962
  -0.04804496 -0.00596324]
 [ 0.25370549  0.16187612 -0.19209506  0.01644268 -0.10753587 -0.00092508
  -0.0845144  -0.00596324]
 [ 0.26274746  0.28040208 -0.15940612  0.01644268 -0.18895451  0.04700405
  -0.11636913 -0.00596324]
 [ 0.22486745  0.35834248 -0.135527    0.01644268 -0.12269946  0.08201607
  -0.13492473 -0.00596324]]
(openpi) a3r@A3R-Omniverse-Sim:~/Interns/internship2024-25/openPi/openpiSource$ python testing.py 
WARNING:2025-02-06 16:38:26,869:jax._src.xla_bridge:987: An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not installed. Falling back to cpu.
WARNING:jax._src.xla_bridge:An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not installed. Falling back to cpu.
Some kwargs in processor config are unused and will not have any effect: time_horizon, action_dim, vocab_size, scale, min_token. 
Some kwargs in processor config are unused and will not have any effect: time_horizon, action_dim, vocab_size, scale, min_token. 
[[ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]
 [ 0.16226726  0.03725068 -0.22036585 -0.01090471  0.02199482 -0.00092508
  -0.0137995  -0.00596324]]
```