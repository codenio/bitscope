#!/bin/bash

python -m pydoc -w bitscope
python -m pydoc -w bitscope.scope
python -m pydoc -w bitscope.device
python -m pydoc -w bitscope.channel
python -m pydoc -w bitscope.metadata
python -m pydoc -w bitscope.trace

mv *.html docs/liberary-reference/