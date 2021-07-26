from secret import get_token

from amplify import BinaryPoly, gen_symbols
from amplify.client import HitachiClient

q = gen_symbols(BinaryPoly, 512, 512)
f = -2 * q[0][0] * q[1][1] - q[0][0] - q[1][1] + 1

client = HitachiClient()
client.token = get_token()
client.parameters.temperature_num_steps = 10
client.parameters.temperature_step_length = 100
client.parameters.temperature_initial = 100.0
client.parameters.temperature_target = 0.02

result = client.solve(f)


