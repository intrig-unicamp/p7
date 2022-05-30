 ################################################################################
 # Copyright 2022 INTRIG
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #     http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 ################################################################################
 
#!/bin/bash

# DIR is this file directory.
DIR="$( pwd )"
output_dir="${DIR}"
     echo "*** Output in ${output_dir}"

docker run -it --rm --entrypoint "" \
     -v "${output_dir}":/workspace \
     -w /workspace p4lang/p4runtime-sh:latest bash \
     -c "source /p4runtime-sh/venv/bin/activate; \
     export PYTHONPATH=/p4runtime-sh:/p4runtime-sh/py_out; \
     python3 -c 'import p4runtime_sh.shell as sh'; \
     python3 p4rt/p4rt.py" \
