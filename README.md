# deep_chess
An attempt at loosely replicating this paper: https://arxiv.org/abs/1711.09667

Successes:
* I trained a model with 85% accuracy identifying "winning" positions on a validation set.
* My model evaluates some concrete use cases sensibly, like being down a piece, certain openings being preferable, etc

Room for improvement:
* The model is big and slow, and it's possible that my minimax algorithm is inefficient. In any case, this makes it difficult to truly evaluate playing performance at good depth.

There is a python script for preprocessing and saving some games downloaded from the online comupter chess database (see above paper for details). 
Note that there should probably be some compressing or smarter storage of the game files, but I haven't encorporated that at this point.

The notebook contains the code for building the neural networks as well as the minimax algorithm and code for playing vs the model.
