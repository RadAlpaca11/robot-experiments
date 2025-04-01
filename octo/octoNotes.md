Followed installation guide from README for gpu.
Had a few issues that were solved with some commands and changing some code to be able to run the test code from README:
```bash
pip install --upgrade scipy
pip install --upgrade jax jaxlib
pip install --upgrade flax
pip install "numpy<2.0"
pip install --upgrade "jax[cuda]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

```python
# Replace this:
PRNGKey = jax.random.KeyArray

# With this:
PRNGKey = jax.random.PRNGKey
```

!pip install mediapy
!pip install opencv-python

python examples/02_finetune_new_observation_action.py --pretrained_path=hf://rail-berkeley/octo-small-1.5 --data_dir=...