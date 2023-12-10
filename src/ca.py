import numpy as np
import copy

class CA:

    '''
        CA stands for Cellular Automata.
    '''
    def __init__(self,
                 n = 10,
                 density = None):

        # Environmental parameters
        self.n = n

        # Initialise experiment
        self._wipe()

        if not density == None:
            for i in range(self.n):
                if np.random.rand() < density:
                    self.env_0[i] = 1

    def _wipe(self):
        '''
            Wipe the experiment
        '''
        self.env_0 = np.zeros(self.n, dtype=int) 
        self._reset()
            
    def _reset(self):
        self.t = 0
        self.env = self.env_0

        self.env_history = []
        self.env_history.append(self.env)

    def run(self, steps = 1):
        for i in range(steps):
            self._step()

    def _step(self):
        self.env = self._update_env(self.env) # Apply rule
        self.env_history.append(self.env)
        self.t = self.t + 1

    def _update_env(self, env):
        # Default _update_env (do nothing).
        new_env = self.env
        return new_env

    def _ind_shift(self, 
                  i, # Current index
                  k  # Index shift
                  ):
        '''
            Implement periodic boundary conditions.
        '''
        return np.mod(i+k, self.n)

class CA_STAR(CA):

    '''
        Example instance of CA.

        Assume k=2 states...
    '''
    def __init__(self, n = 10, density = None, enc = '1110', r = 1):
        CA.__init__(self, n = n, density = density)
        self.enc = enc
        self.r = r

        # Encoding check
        # ...
        if not len(enc) == 2*(r+1):
            raise Exception("Encoding not compatible with r value.")


    def _update_env(self, env):
        # Update rule based on totalistic encoding (see Wolfram)

        new_env = np.zeros(len(env),dtype=int)
        for i in range(len(env)):
            # Define cell update rule:
            total = 0
            for j in range(-self.r,self.r+1):
                total = total + env[self._ind_shift(i,j)]

            new_env[i] = int(self.enc[-(total+1)])

        return new_env
    
    def _set_enc(self, enc):
        self.enc = enc