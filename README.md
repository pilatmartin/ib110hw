This library was created for the course **IB110 - Introduction to Informatics** at [MUNI FI](https://www.fi.muni.cz/).

# INSTALLATION

Python version >=3.6 is required in order to use the library.
Using virtual environment for installation is of course optional, but recommended.

```sh
# Bash
$ python3 -m venv <name> 
$ source <name>/bin/activate
$ pip install ib110hw
```

```powershell
# Windows Powershell
PS> py -m venv <name> 
PS> <name>\Scripts\Activate.ps1
PS> pip install ib110hw
```

Below is an overview of how these computational models can be used. Further documentation is located in the files with the implementation.

# FINITE AUTOMATA

This library supports **deterministic** and **nondeterministic** finite automata. You can find the implementation of these models in the module `automaton`. Consider the class located in the `base.py` as abstract, its only purpose is to avoid duplicity in the implementation of these models.

In order to create an automaton you will need to specify the five-tuple `(Q, Σ, δ, q0, F)`, where:

- The set of states `Q` is represented by `Set[str]`
- The set of alphabet symbols `Σ` is represented by `Set[str]`
- The transition function `δ` is represented by either `DFATransitions` or `NFATransitions`. These types are described below.
- The set of final states `F` is represented by `Set[str]`

`DFA` and `NFA` objects can be created in two ways:

1. If you know exactly how the automaton should look like you can create it directly - section **Example use-case of DFA** and **Example use-case of NFA**.
2. If you are implementing an algorithm, for example, you can use helper functions - described in section **DFA helper functions** and **NFA helper functions**.

## Deterministic finite automata (DFA)

The implementation for DFA can be found in the file `automaton/dfa.py`.

### Example use-case of DFA

The `DFATransitions` is an alias to `Dict[str, Dict[str, str]]`. Keys of this dictionary are symbols where the transition begins. Values are nested dictionaries with alphabet symbols as keys and states where the transition ends as values.

#### Example of a DFA transition function

</br>

[![DFA transition function example](https://mermaid.ink/img/pako:eNpFj7EOgzAMRH8l8gRSkIAxlTp1bJd2bDpExJQIQlASBoT497qBqp78zmfLt0LjNIKAt1dTx653OTKqUGVZqPL8oJqo_tLB5ZO9WFGcyffzE1a8TFq9-9IkxGVAWmCtGYbCTaoxcRElp4F3Pf6VE3Cw6K0ymr5Z0wGIHVqUIKjVyvcS5LiRT83RPZaxARH9jBzmSauIF6MohAXRqiGQitpE5297vJRy-wDaf0jH?type=png)](https://mermaid.live/edit#pako:eNpFj7EOgzAMRH8l8gRSkIAxlTp1bJd2bDpExJQIQlASBoT497qBqp78zmfLt0LjNIKAt1dTx653OTKqUGVZqPL8oJqo_tLB5ZO9WFGcyffzE1a8TFq9-9IkxGVAWmCtGYbCTaoxcRElp4F3Pf6VE3Cw6K0ymr5Z0wGIHVqUIKjVyvcS5LiRT83RPZaxARH9jBzmSauIF6MohAXRqiGQitpE5297vJRy-wDaf0jH)

Transition shown above can be written like so:

```python
transition_fn: DFATransitions = {
    "s1": { # from s1
        "0": "s2", # via 0 to s2
        "1": "s2", # via 1 to s2
    },
}
```

#### More complex DFA example

</br>

[![More complex DFA example](https://mermaid.ink/img/pako:eNpdkT1vwyAQhv8KusmWbMn4Y6FSp4zp0oxxBmTOCQo2FsaDFeW_5-IWmpSJ5-F4OR036KxCEHB2crqw_Xc7MlpzkSRzkaa_xIl4pJKojFQRVZFqojpSkxA26ZND7pGdWJ5_UmbIJuSbKUN-NNWLKTbThFefNdm747GqDt1EU70Y_nar-Z-0-dmvBqld1mtjcjvJTvtVFBkdOHvFP_MBGQzoBqkVTfG2BYC_4IAtCNoq7OVifAvteKdSuXh7WMcOhHcLZrBMSnrcaUnzH0D00sxkUWlv3dfPz3R27PUZ7g-ne3N9?type=png)](https://mermaid.live/edit#pako:eNpdkT1vwyAQhv8KusmWbMn4Y6FSp4zp0oxxBmTOCQo2FsaDFeW_5-IWmpSJ5-F4OR036KxCEHB2crqw_Xc7MlpzkSRzkaa_xIl4pJKojFQRVZFqojpSkxA26ZND7pGdWJ5_UmbIJuSbKUN-NNWLKTbThFefNdm747GqDt1EU70Y_nar-Z-0-dmvBqld1mtjcjvJTvtVFBkdOHvFP_MBGQzoBqkVTfG2BYC_4IAtCNoq7OVifAvteKdSuXh7WMcOhHcLZrBMSnrcaUnzH0D00sxkUWlv3dfPz3R27PUZ7g-ne3N9)

```python
from ib110hw.automaton.dfa import DFA, DFATransitions

dfa_transitions: DFATransitions = {
    "s1": {
        "1": "s2",
        "0": "s4"
    },
    "s2": {
        "1": "s3",
        "0": "s5"
    },
    "s3": {
        "1": "s5",
        "0": "s5"
    },
    "s4": {
        "1": "s5",
        "0": "s3"
    },
    "s5": {
        "1": "s5",
        "0": "s5"
    },
}

automaton = DFA(
    states={"s1", "s2", "s3", "s4", "s5" },
    alphabet={"1", "0"},
    initial_state="s1",
    final_states={"s3"},
    transitions=dfa_transitions,
)
```

#### Helper functions for DFA

Below are described some use-cases of the implemented helper functions. If you want to learn more about them, check the `automaton/dfa.py` file containing the implementation with further documentation.

##### Helper functions for getting information about a DFA

The following examples will use the `DFA` object created above.

```python
# returns next state from the provided state by symbol
automaton.get_transition("s1", "1") # returns "s2"
automaton.get_transition("s1", "0") # returns "s4"
```

```python
# returns set of symbols between two (directly) adjacent states
automaton.get_symbols_between_states("s1", "s2") # returns {"1"}
automaton.get_symbols_between_states("s3", "s5") # returns {"1", "0"}
automaton.get_symbols_between_states("s1", "s3") # returns set()
```

```python
# returns True if the given string is accepted by the automaton, False otherwise
# IMPORTANT: the automaton needs to be valid (see below) to be able to test 
automaton.is_accepted("11") # False
automaton.is_accepted("00") # False
automaton.is_accepted("10") # True
```

```python
# Checks whether the DFA is valid:
#     1. The states set is not empty.
#     2. The initial state is in states.
#     3. Final states are subset of states.
#     4. The alphabet does not contain ε ('').
#     5. The transition function contains characters only from its alphabet.
#     6. The transition function contains states only from its states set.
#     7. The transition function is total.
automaton.is_valid() # returns True
```

##### Helper functions for altering a DFA

The `DFA` class contains some helper functions to alter the automata if you wish to implement an algorithm for example. Some use-cases are described below, with pictures of automata to show how it progressively changes.

```python
# all params are optional, but to be able to check whether it accepts a given input,
# it needs to have them all defined
showcase_dfa: DFA = DFA(alphabet={"a", "b", "c"}) 

# adds a singular state to automaton
# second param specifies if the state is final - defaults to False
showcase_dfa.add_state("s1", False) # returns True - automaton was altered
showcase_dfa.add_state("s1") # returns False - nothing changed, since state s1 already exists
```

</br>

[![DFA object with a single state](https://mermaid.ink/img/pako:eNoljbsOwjAQBH_F2iqR0qR1TQkNtNeccgexwHbkR4Gi_DsHdKvd0c6OJYvC41F4W935Ssk5V-dhqPM4YkLUEjmIEft3IrRVoxK8ReHyJFA6jOPe8u2dFvhWuk7om3DTU2A7jvB3flVrVULL5fJX_szHB1eJKhw?type=png)](https://mermaid.live/edit#pako:eNoljbsOwjAQBH_F2iqR0qR1TQkNtNeccgexwHbkR4Gi_DsHdKvd0c6OJYvC41F4W935Ssk5V-dhqPM4YkLUEjmIEft3IrRVoxK8ReHyJFA6jOPe8u2dFvhWuk7om3DTU2A7jvB3flVrVULL5fJX_szHB1eJKhw)

```python
showcase_dfa.add_state("s2") 
showcase_dfa.add_state("s4") 
```

</br>

[![DFA object with three disjointed states](https://mermaid.ink/img/pako:eNplkbEKwjAQhl8lHAgKDTRtXSI4iKuTjllCc2qwbUqaDkV8d68VEtRM-b78Obi7J9TOIEi4ed3f2eWgOkZntWJDvl4P-WbzEYMgEpEKoiJSRVTNlD4LxrngfE_RJIsoy2-ZL3KbZDknsz8tYrZKsoqy_Jbi9_v2t6rqSM8dhKlB6phdbdNw1-vahknmGT1498BkdpBBi77V1tDMnksNCHdsUYGkq9H-oUB1L8rpMbjz1NUggx8xg7E3OuDRahp1C_Kqm4EsGhucP32WsOzi9QbHTGp1?type=png)](https://mermaid.live/edit#pako:eNplkbEKwjAQhl8lHAgKDTRtXSI4iKuTjllCc2qwbUqaDkV8d68VEtRM-b78Obi7J9TOIEi4ed3f2eWgOkZntWJDvl4P-WbzEYMgEpEKoiJSRVTNlD4LxrngfE_RJIsoy2-ZL3KbZDknsz8tYrZKsoqy_Jbi9_v2t6rqSM8dhKlB6phdbdNw1-vahknmGT1498BkdpBBi77V1tDMnksNCHdsUYGkq9H-oUB1L8rpMbjz1NUggx8xg7E3OuDRahp1C_Kqm4EsGhucP32WsOzi9QbHTGp1)

```python
# adds a transition from s1 to s2 by '1'
showcase_dfa.add_transition("s1", "s2", "1") # returns True - it changed the automaton

# this will not change the automaton, since transition from s1 by '1' already exists
showcase_dfa.add_transition("s1", "s4", "1") # returns False - nothing changed
```

</br>

[![DFA object with three states, but one is disconnected (1)](https://mermaid.ink/img/pako:eNplkbEKwjAQhl8lHAgVGmjaukRwctRF1yyhOTXYNiVNhyK-u9eKKWqmfF_-HMndAypnECRcve5u7HBSLaO1WrE-S5I-W6_fohdEIlJOlEcqicqJPlnGueB8R7mlXB5l8S2zWW4WWUzJ9E-LmC0XWUZZfEvxe33zW1W1pKfnhrFG-i672LrmrtOVDaPMUjrw7o6L2UIKDfpGW0MNe8w1INywQQWStkb7uwLVPimnh-DOY1uBDH7AFIbO6IB7q6nPDciLrnuyaGxw_viewDyI5wsQuGoT?type=png)](https://mermaid.live/edit#pako:eNplkbEKwjAQhl8lHAgVGmjaukRwctRF1yyhOTXYNiVNhyK-u9eKKWqmfF_-HMndAypnECRcve5u7HBSLaO1WrE-S5I-W6_fohdEIlJOlEcqicqJPlnGueB8R7mlXB5l8S2zWW4WWUzJ9E-LmC0XWUZZfEvxe33zW1W1pKfnhrFG-i672LrmrtOVDaPMUjrw7o6L2UIKDfpGW0MNe8w1INywQQWStkb7uwLVPimnh-DOY1uBDH7AFIbO6IB7q6nPDciLrnuyaGxw_viewDyI5wsQuGoT)

```python
# this method either adds a transition like above, or overwrites the existing one
# the transition from s1 by '1' gets redirected to the state s4
dfa_showcase.set_transition("s1", "s4", "1") # returns None
```

</br>

[![DFA object with three states, but one is disconnected (2)](https://mermaid.ink/img/pako:eNplkT8LwjAQxb9KOBAUGmjaukRwEFcnHbOE5tRg25Q0HYr43b1WTP2TKe93L4_L3R1KZxAkXLxur-y0Uw2js1iwLl0uu3S1eoFOkBJRZaSyqApSxajeXsa54HxLlTkuizD_hukE1zPMR2fyh0X0fqQWEebfUPw-X_-mqobw2G4YKqTvsrOtKu5aXdowyDShgnc3nMkGEqjR19oaGth9yoBwxRoVSLoa7W8KVPMgn-6DOw5NCTL4HhPoW6MD7q2mOdcgz7rqiKKxwfnDawPTIh5PBxxqDQ?type=png)](https://mermaid.live/edit#pako:eNplkT8LwjAQxb9KOBAUGmjaukRwEFcnHbOE5tRg25Q0HYr43b1WTP2TKe93L4_L3R1KZxAkXLxur-y0Uw2js1iwLl0uu3S1eoFOkBJRZaSyqApSxajeXsa54HxLlTkuizD_hukE1zPMR2fyh0X0fqQWEebfUPw-X_-mqobw2G4YKqTvsrOtKu5aXdowyDShgnc3nMkGEqjR19oaGth9yoBwxRoVSLoa7W8KVPMgn-6DOw5NCTL4HhPoW6MD7q2mOdcgz7rqiKKxwfnDawPTIh5PBxxqDQ)

```python
showcase_dfa.set_transition("s1", "s2", "1") 
showcase_dfa.set_transition("s1", "s4", "0") 
```

</br>

[![DFA object with three states](https://mermaid.ink/img/pako:eNptkUsLwjAQhP9KWBAsNNCXlwiePOpFr7mEZtVg25Q0PRTpf3fbYusrp8yXySTMPiC3GkHA1an6xg4nWTFaqxVrovW6iYJgAk1MKp5VQiqZVUYqG9TLyziPOd-R741EI8mWB5LZln7CyblZYDo4wx_8NzWbYfoJ4-_rm-9UWREevuu7AqkAdjFFwW2tcuM7EYV04OwdF7KFEEp0pTKaKnyMGeBvWKIEQVut3F2CrHryqdbbc1flILxrMYS21srj3ihqvgRxUUVDFLXx1h2nmYyj6Z-YSm4K?type=png)](https://mermaid.live/edit#pako:eNptkUsLwjAQhP9KWBAsNNCXlwiePOpFr7mEZtVg25Q0PRTpf3fbYusrp8yXySTMPiC3GkHA1an6xg4nWTFaqxVrovW6iYJgAk1MKp5VQiqZVUYqG9TLyziPOd-R741EI8mWB5LZln7CyblZYDo4wx_8NzWbYfoJ4-_rm-9UWREevuu7AqkAdjFFwW2tcuM7EYV04OwdF7KFEEp0pTKaKnyMGeBvWKIEQVut3F2CrHryqdbbc1flILxrMYS21srj3ihqvgRxUUVDFLXx1h2nmYyj6Z-YSm4K)

```python
showcase_dfa.add_state("s3")
showcase_dfa.add_transition("s2", "s3", "1")
showcase_dfa.add_transition("s4", "s3", "0")

# add the final state
showcase_dfa.add_state("s5", True)

showcase_dfa.add_transition("s2", "s5", "0")
showcase_dfa.add_transition("s3", "s5", "0")
showcase_dfa.add_transition("s3", "s5", "1")
showcase_dfa.add_transition("s4", "s3", "1")
showcase_dfa.add_transition("s5", "s5", "0")
showcase_dfa.add_transition("s5", "s5", "1")
```

</br>

[![DFA with missing initial state](https://mermaid.ink/img/pako:eNpdkU2LgzAQhv9KGCgoKBg_Lin01GN76R43ewhm2oaqkRgPUvrfd7SYtZtTnieTN0PmCbXVCAJuTvV3drrIjtHa7diQRdGQxfFbDJyIB8qJ8kAFURGoJCoDVRFhFc-8if5mPyxNDxS7xhPyxeTrE8EUG5MtplofnmuST8dDVbk2FEyxMfzjVvU_SXbU6HzipwapY3Y1TZPaXtXGTyJL6MDZB_6ZPSTQomuV0fSdzyUD_B1blCBoq5V7SJDdi-rU6O3X1NUgvBsxgbHXyuPRKJpCC-KqmoEsauOtO7_ns4zp9QvrunKd?type=png)](https://mermaid.live/edit#pako:eNpdkU2LgzAQhv9KGCgoKBg_Lin01GN76R43ewhm2oaqkRgPUvrfd7SYtZtTnieTN0PmCbXVCAJuTvV3drrIjtHa7diQRdGQxfFbDJyIB8qJ8kAFURGoJCoDVRFhFc-8if5mPyxNDxS7xhPyxeTrE8EUG5MtplofnmuST8dDVbk2FEyxMfzjVvU_SXbU6HzipwapY3Y1TZPaXtXGTyJL6MDZB_6ZPSTQomuV0fSdzyUD_B1blCBoq5V7SJDdi-rU6O3X1NUgvBsxgbHXyuPRKJpCC-KqmoEsauOtO7_ns4zp9QvrunKd)

The `dfa` pictured above is still not a valid DFA, since it lacks an initial state. This can be fixed by simply editing the `initial_state` property. The automaton is now equivalent to the **More complex example** shown above.

```python
dfa_showcase.is_valid() # returns False

dfa_showcase.initial_state = "s1"

dfa_showcase.is_valid() # returns True
```

</br>

[![Valid DFA object](https://mermaid.ink/img/pako:eNpdkT1vwyAQhv8KusmWbMn4YyFSpoztkoxxB2QuDfIHFsaDFeW_50ILTcrE83C8nI4bdEYhCPi2cr6yj2M7MVpLkSRLkaa_xIl4pJKojFQRVZFqojpSkxA26ZND7pl9sTzfU2bIJuTelCE_murFFN404dVnTfbueKyqQzfRVC-Gv91q_id5v7htQGqXXfQw5GaWnXabKDI6sKbHP7ODDEa0o9SKpnjzAeCuOGILgrZK2r6FdrpTnVydOW1TB8LZFTNYZyUdHrSk4Y8gLnJYyKLSztjPn2_xv3N_AFuwcV8?type=png)](https://mermaid.live/edit#pako:eNpdkT1vwyAQhv8KusmWbMn4YyFSpoztkoxxB2QuDfIHFsaDFeW_50ILTcrE83C8nI4bdEYhCPi2cr6yj2M7MVpLkSRLkaa_xIl4pJKojFQRVZFqojpSkxA26ZND7pl9sTzfU2bIJuTelCE_murFFN404dVnTfbueKyqQzfRVC-Gv91q_id5v7htQGqXXfQw5GaWnXabKDI6sKbHP7ODDEa0o9SKpnjzAeCuOGILgrZK2r6FdrpTnVydOW1TB8LZFTNYZyUdHrSk4Y8gLnJYyKLSztjPn2_xv3N_AFuwcV8)

```python
# strings can now be tested
automaton.is_accepted("11") # True
automaton.is_accepted("00") # True
automaton.is_accepted("10") # False
```

Transitions and states can also be removed:

```python
# removes the transition from s1 by '0'
dfa_showcase.remove_transition("s1", "0")
```

</br>

[![DFA object with removed transition](https://mermaid.ink/img/pako:eNpdkT1rwzAQhv-KOAjYYIM_FxUyZUyWZKw7COvSCH_IyPJgQv57L3KlJtWk59Hx6ri7Q6slAodvI6YbO56bkdGZsyiaszj-pZwoD1QQFYFKojJQRVQFqiPCOn6yz_1kXyxN95TpswlzZwqfH0z5YjJnav_rsyZ5c7vdFrbJyjcUTPli8rew-n-Y87Nde6SO2VX1faon0Sq78iyhB6M7_DMfkMCAZhBK0iDvLgDsDQdsgNNVCtM10IwPqhOL1Zd1bIFbs2ACyySFxYMSNP8B-FX0M1mUympz2jbjFvT4AUZlcck?type=png)](https://mermaid.live/edit#pako:eNpdkT1rwzAQhv-KOAjYYIM_FxUyZUyWZKw7COvSCH_IyPJgQv57L3KlJtWk59Hx6ri7Q6slAodvI6YbO56bkdGZsyiaszj-pZwoD1QQFYFKojJQRVQFqiPCOn6yz_1kXyxN95TpswlzZwqfH0z5YjJnav_rsyZ5c7vdFrbJyjcUTPli8rew-n-Y87Nde6SO2VX1faon0Sq78iyhB6M7_DMfkMCAZhBK0iDvLgDsDQdsgNNVCtM10IwPqhOL1Zd1bIFbs2ACyySFxYMSNP8B-FX0M1mUympz2jbjFvT4AUZlcck)

```python
# removes the state s3 and every transition associated with it
dfa_showcase.remove_state("s")
```

</br>

[![DFA object after removing a state](https://mermaid.ink/img/pako:eNplkT1rwzAQhv-KOAjYYIM_5EWFTh3bJRnrDsK6NCK2ZSR5MCH_vRe1kkurSc-j471Dd4PBKAQBn1YuF_Z67GdGx1VZ5qo8_6GaqE7UEDWRDgfmWhJteuZEPFGXEXb5g2P0O_tgZflMsTGesA6m2UObJNvYl0wVTPer96Os-KfrVMt3yZOMkTw16eK8f_OCd34bkUZnZz2OpVnkoP0mqoIerLnibp6ggAntJLWiT72FAPAXnLAHQVcl7bWHfr5TnVy9OW3zAMLbFQtYFyU9vmhJu5hAnOXoyKLS3ti37y2FZd2_AMruc3E?type=png)](https://mermaid.live/edit#pako:eNplkT1rwzAQhv-KOAjYYIM_5EWFTh3bJRnrDsK6NCK2ZSR5MCH_vRe1kkurSc-j471Dd4PBKAQBn1YuF_Z67GdGx1VZ5qo8_6GaqE7UEDWRDgfmWhJteuZEPFGXEXb5g2P0O_tgZflMsTGesA6m2UObJNvYl0wVTPer96Os-KfrVMt3yZOMkTw16eK8f_OCd34bkUZnZz2OpVnkoP0mqoIerLnibp6ggAntJLWiT72FAPAXnLAHQVcl7bWHfr5TnVy9OW3zAMLbFQtYFyU9vmhJu5hAnOXoyKLS3ti37y2FZd2_AMruc3E)

##### Visualization

`DFA` objects can be visualized in two ways: `print` and `automaton_to_graphviz`. The following example uses the `automaton` object from the **More complex example** section.

```python
from ib110.automaton.utils import automaton_to_graphviz

print(automaton) 
# alphabet: 0,1
# states: s1,s5,s3,s2,s4
# final states: s3
# 
#      DFA      |    0    |    1    
# ----------------------------------
# -->  s1       |   s4    |   s2    
#      s2       |   s5    |   s3    
# <--  s3       |   s5    |   s5    
#      s4       |   s3    |   s5    
#      s5       |   s5    |   s5   
```

The following produces a .dot (graphviz) file which can then be viewed by either downloading an extension/plugin ([vscode link](https://marketplace.visualstudio.com/items?itemName=joaompinto.vscode-graphviz), [jetbrains link](https://plugins.jetbrains.com/plugin/10312-dot-language)) or by going [here](https://dreampuf.github.io/GraphvizOnline) and pasting the result.

```python
automaton_to_graphviz(automaton, path="./automaton.dot")
```

## Nondeterministic finite automata (NFA)

The implementation for the NFA can be found in the file `nfa.py` with a description of each function.

### Example use-case of NFA

Transition function of an NFA is described by the `NFATransitions`. It is an alias to `Dict[str, Dict[str, Set[str]]]`. It is similar to the `DFATransitions` but instead of the next-state string, there is a **set** of next-state strings.

#### Example of a NFA transition function

</br>

[![](https://mermaid.ink/img/pako:eNplkD0PgjAQhv9KcxMkkPCx1cTJURcdxaGhhzS0lJQyEMJ_9yyog536PNf3ctcFaisRODydGFp2vlY9ozPmUTTmcbxTQVR8qSQq37RzdmcPlqZHSn3ShFkwxZ8pt1zwo581UgPWKK1TO4ha-ZlnCRWc7fBnDpCAQWeEkjTrEhqAb9FgBZyuUriugqpf6Z2YvL3NfQ3cuwkTmAYpPJ6UoBUN8EbokSxK5a27bMuHP1hf2DVPmA?type=png)](https://mermaid.live/edit#pako:eNplkD0PgjAQhv9KcxMkkPCx1cTJURcdxaGhhzS0lJQyEMJ_9yyog536PNf3ctcFaisRODydGFp2vlY9ozPmUTTmcbxTQVR8qSQq37RzdmcPlqZHSn3ShFkwxZ8pt1zwo581UgPWKK1TO4ha-ZlnCRWc7fBnDpCAQWeEkjTrEhqAb9FgBZyuUriugqpf6Z2YvL3NfQ3cuwkTmAYpPJ6UoBUN8EbokSxK5a27bMuHP1hf2DVPmA)

Transition shown above can be implemented like so:

```python
transition_fn: NFATransitions = {
    "s1": {
        "0": {"s2", "s3"},
        "1": set(), # specifying this is unnecessary
    },
}
```

#### More complex NFA example

</br>

[![](https://mermaid.ink/img/pako:eNpNkD0PgjAQhv9KcxMkkPA11cTJURcdxaGhhzQWSkoZCOG_e1ZAO_V5enkvfWeojETg8LSib9j5WnaMzpAGwZCG4UoZUbZTHhDm4c4FYfGhlZM7e7A4PlLKlkaYepNtibvJ_2YSb4otdzd-xtvBTRppBauV1rHpRaXcxJOIHqx54c8cIIIWbSuUpN_NPgBcgy2WwOkqhX2VUHYLzYnRmdvUVcCdHTGCsZfC4UkJKqUFXgs9kEWpnLGXb12-teUNz6daTA?type=png)](https://mermaid.live/edit#pako:eNpNkD0PgjAQhv9KcxMkkPA11cTJURcdxaGhhzQWSkoZCOG_e1ZAO_V5enkvfWeojETg8LSib9j5WnaMzpAGwZCG4UoZUbZTHhDm4c4FYfGhlZM7e7A4PlLKlkaYepNtibvJ_2YSb4otdzd-xtvBTRppBauV1rHpRaXcxJOIHqx54c8cIIIWbSuUpN_NPgBcgy2WwOkqhX2VUHYLzYnRmdvUVcCdHTGCsZfC4UkJKqUFXgs9kEWpnLGXb12-teUNz6daTA)

```python
from ib110hw.automaton.nfa import NFA, NFATransitions

nfa_transitions: NFATransitions = {
    "s1": {
        "1": { "s2" },
        "0": { "s4" },
    },
    "s2": {
        "1": { "s3" },
    },
    "s4": {
        "0": { "s3" },
    },
}

automaton = NFA(
    states={"s1", "s2", "s3", "s4", "s5" },
    alphabet={"1", "0"},
    initial_state="s1",
    final_states={"s3"},
    transitions=nfa_transitions,
)

automaton.is_accepted("11") # True
automaton.is_accepted("00") # True
automaton.is_accepted("10") # False
```

#### NFA helper functions

Below are described some use-cases of the implemented helper functions. If you want to learn more about them, check the `automaton/nfa.py` file containing the implementation with further documentation.

##### Helper functions for getting information about an NFA

All of the NFA class methods for getting information about the automaton. The difference is only in the `is_valid` method which has different requirements:

```python
#Checks whether the NFA is valid:
#    1. States set is not empty.
#    2. Initial state is in states.
#    3. Final states are subset of states.
#    4. The transition function contains characters only from its alphabet.
#    5. The transition function contains states only from its states set.
automaton.is_valid() # returns true
```

##### Helper functions for altering an NFA

All of the NFA class methods for altering the automaton are used the same way as with DFA class instead of one:

```python
# this method either adds a transition, or overwrites the existing one
# the difference compared to the DFA is that it takes a *set* of next states
automaton.set_transition("s1", {"s2"}, "1")
```

# TURING MACHINE

This library supports **deterministic** and **multi-tape** Turing machines. You can find the implementation in the module `turing`. Consider the class located in the base.py as abstract, its only purpose is to avoid duplicity in the implementation of these models.

In order to create a Turing machine you will need to specify the seven-tuple `(Q, Σ, Γ, δ, q0, q_acc, q_rej)`, where:

- The set of states `Q` is represented by `Set[str]`
- The set of alphabet symbols `Σ` is represented by `Set[str]`
- The transition function `δ` is represented by either `DTMTransitions` or `MTMTransitions`. These types are described below.
- The initial state `q0` is represented by `str`
- The accepting state `q_acc` is represented by `str`
- The rejecting state `q_rej` is represented by `str`

## Tape

The implementation of the tape for the Turing machine can be found in the file `tape.py`. The tape class is only used internally by the `DTM` and `MTM` objects - you will *probably* not use it directly.

```python
from ib110hw.turing.tape import Tape

tape: Tape = Tape()
tape.write("Hello")
print(tape)         # | H | e | l | l | o |   |
                    #   ^

tape.move_left()
print(tape)         # |   | H | e | l | l | o |   |
                    #   ^

tape.move_right()
tape.move_right()
print(tape)         # |   | H | e | l | l | o |   |
                    #           ^

tape.write_symbol("a")
print(tape)         # |   | H | a | l | l | o |   |
                    #           ^

tape.clear()        # |   |
                    #   ^

```

The module `tape` also contains enum for the direction of tape head:

```python
class Direction(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1
    
    # shorthand aliases
    L = -1
    S = 0
    R = 1

    def __repr__(self):
        return self.name
```

## Deterministic Turing Machine (DTM)

The following DTM checks whether the input string is a palindrome:

```python
from ib110hw.turing.dtm import DTM, DTMTransitions

transitions: DTMTransitions = {
    "init": {
        ">": ("mark", ">", Direction.RIGHT),
    },
    "mark": {
        "a": ("foundA", "X", Direction.RIGHT),
        "b": ("foundB", "X", Direction.RIGHT),
        "X": ("accept", "X", Direction.STAY),
        "": ("accept", "", Direction.STAY),
    },
    "foundA": {
        "a": ("foundA", "a", Direction.RIGHT),
        "b": ("foundA", "b", Direction.RIGHT),
        "X": ("checkA", "X", Direction.LEFT),
        "": ("checkA", "", Direction.LEFT),
    },
    "checkA": {
        "a": ("back", "X", Direction.LEFT),
        "b": ("reject", "b", Direction.STAY),
        "X": ("accept", "X", Direction.STAY),
    },
    "foundB": {
        "a": ("foundB", "a", Direction.RIGHT),
        "b": ("foundB", "b", Direction.RIGHT),
        "X": ("checkB", "X", Direction.LEFT),
        "": ("checkB", "", Direction.LEFT),
    },
    "checkB": {
        "a": ("reject", "a", Direction.STAY),
        "b": ("back", "X", Direction.LEFT),
        "X": ("accept", "X", Direction.STAY),
    },
    "back": {
        "a": ("back", "a", Direction.LEFT),
        "b": ("back", "b", Direction.LEFT),
        "X": ("mark", "X", Direction.RIGHT)
    }
}

machine: DTM = DTM(
    states={"init", "mark", "gotoEndA", "checkA", "gotoEndB", "checkB", "accept", "reject"},
    input_alphabet={"a", "b"},
    acc_state="accept",
    rej_state="reject",
    initial_state="init",
    transitions=transitions
)

machine.write_to_tape("aabbabbaa")
```

### DTM Transition function

A DTM transition function is represented by a nested dictionary defined by the type `DTMTransitions`.
The keys of this dictionary are **states** of the turing machine, and values are dictionaries with **read symbols** as keys and a tuple containing the **next state**, **symbol to be written** and **the tape head direction** as values.

Rule `δ(init, >) -> (next, >, 1)` can be defined like so:

```python
function: DTMransitions = {
    "init": {
        ">": ("next", ">", Direction.RIGHT)
        }
}
```

### Loading From a File

DTM can also be loaded from a file. Format is shown below:

```
# name of the initial state
init init

# name of the accepting state
acc acc

# name of the rejecting state
rej rej

# alphabet characters without start_symbol
alphabet a b

---

# current read -> next write direction(L, R, S)
# ! underscore (_) is used to depict <space> !
init    > -> mark   > R
mark    a -> foundA X R
mark    b -> foundB X R
mark    X -> acc    X S
mark    _ -> acc    _ S
foundA  a -> foundA a R
foundA  b -> foundA b R
foundA  X -> checkA X L
foundA  _ -> checkA _ L
checkA  a -> back   X L
checkA  b -> acc    b S
checkA  X -> rej    X S
foundB  a -> foundB a R
foundB  b -> foundB b R
foundB  X -> checkB X L
foundB  _ -> checkB _ L
checkB  a -> reject a S
checkB  b -> reject X L
checkB  X -> reject X S
back    a -> back   a L
back    b -> back   b L
back    X -> mark   X R

```

The file above can then be simply loaded using the `import_dtm(...)`:

```python
from ib110hw.turing.utils import import_dtm

machine = import_dtm("./dtm_file")
```

## Multi-tape Turing Machine (MTM)

On top of the properties required to create DTM, you will need to specify the number of tapes as well. The default tape count is set to 2.

The following MTM has the same function as the DTM above:

```python
from ib110hw.turing.mtm import MTM, MTMTransitions
from ib110hw.turing.tape import Direction

transitions: MTMTransitions = {
    "init": {
        (">", ""): ("copy", (">", ">"), (Direction.R, Direction.R))
    },
    "copy": {
        ("a", ""): ("copy", ("a", "a"), (Direction.R, Direction.R)),
        ("b", ""): ("copy", ("b", "b"), (Direction.R, Direction.R)),
        ("", ""): ("goToStart", ("", ""), (Direction.L, Direction.S)),
    },
    "goToStart": {
        ("a", ""): ("goToStart", ("a", ""), (Direction.L, Direction.S)),
        ("b", ""): ("goToStart", ("b", ""), (Direction.L, Direction.S)),
        (">", ""): ("check", (">", ""), (Direction.R, Direction.L))
    },
    "check": {
        ("a", "a"): ("check", ("a", "a"), (Direction.R, Direction.L)),
        ("b", "b"): ("check", ("b", "b"), (Direction.R, Direction.L)),
        ("", ">"): ("accept", ("", ">"), (Direction.S, Direction.S)),
        ("a", "b"): ("reject", ("a", "b"), (Direction.S, Direction.S)),
        ("b", "a"): ("reject", ("b", "a"), (Direction.S, Direction.S)),
    }
}

machine: MTM = MTM(
    states={"init", "goToEnd", "goToStart", "check", "accept", "reject"},
    initial_state="init",
    input_alphabet={"a", "b"},
    acc_state="accept",
    rej_state="reject",
    transitions=transitions)

machine.write_to_tape("aabbabbaa")
```

### MTM Transition Function

A MTM transition function is represented by a nested dictionary defined by the type `MTMTransitions`. Compared to `DTMTransitions`, it takes a tuple of read symbols instead of a singular symbol and a tuple of directions instead of a singular direction. Length of these tuples is the amount of tapes.

Rule `δ(init, (>, ␣)) = (next, (>, a), (1, 0))` can be defined like so:

```python
function: MTMransitions = {
    "init": {
        (">", ""): ("next", (">", "a"), (Direction.RIGHT, Direction.LEFT))
        }
}
```

MTM can also be loaded from a file. Format is shown below:

```
# name of the initial state
init init

# name of the accepting state
acc acc

# name of the rejecting state
rej rej

# alphabet characters without start_symbol
alphabet a b c

# the amount of tapes (>= 2)
tapes 2

---

# current (reads) -> next [writes] [directions]([L(eft), R(ight), S(tay)])
# ! _ (underscore) is used to depict <space> !
# such spacing is not required
init        (> _) -> copy         (> _) (R S)
copy        (a _) -> copy         (a a) (R R)
copy        (b _) -> copy         (b b) (R R)
copy        (_ _) -> goToStart    (_ _) (L S)
goToStart   (a _) -> goToStart    (a _) (L S)
goToStart   (b _) -> goToStart    (b _) (L S)
goToStart   (> _) -> check        (> _) (R L)
check       (a a) -> check        (a a) (R L)
check       (b b) -> check        (b b) (R L)
check       (_ _) -> acc          (_ _) (S S)
check       (a b) -> rej          (a b) (S S)
check       (b a) -> rej          (b a) (S S)

```

The file above can then be simply loaded using the `import_mtm(...)`:

```python
from ib110hw.turing.utils import import_mtm

machine = import_mtm("./mtm_file")
```

# DTM and MTM Simulation

You can simulate the Turing machine using the provided function `simulate(...)`. By default, every step of the Turing machine will be printed to console with 0.5s delay in-between. This behavior can be changed by setting the `to_console` and `delay` parameters. If the parameter `to_console` is set to `False`, the delay will be ignored.

```python
machine.simulate(to_console=True, delay=0.3) # True
```

There is also an option to simulate the calculation step-by-step, i.e., the TM will wait for user input (arrow keys). It allows for going back and forward in the calculation. This can be enabled by setting the `step_by_step` parameter to `True`. The `delay` and `to_console` parameters are ignored.

```python
machine.simulate(step_by_step=True)
```

If you want to look at the whole history, you can set parameter `to_file` to `True`. Every step will be printed to file based on the path provided in the parameter `path`. Default path is set to `./simulation.md`.

```python
machine.simulate(to_console=False, to_file=True, path="~/my_simulation.md") 
```

The `BaseTuringMachine` class contains the attribute `max_steps` to avoid infinite looping. By default, it is set to 100. The computation will stop if the simulation exceeds the value specified by this attribute. This can be an issue on larger inputs, so setting it to a bigger number may be needed.

```python
turing.max_steps = 200
```

### Simulation in PyCharm

For the optimal visualization of the simulation in PyCharm you need to **enable** the `Terminal emulation`.

You can do so by going to `Run > Edit configurations ...` and then checking the `Emulate terminal in output console` box.
