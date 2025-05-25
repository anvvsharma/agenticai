
### Create a new Conda environment with Python 3.11
    $ conda create -p day01 python=3.11

### Below is the output that generates from the above command

    conda create -p day01 python=3.11
    Retrieving notices: done
    Channels:
    - defaults
    Platform: osx-arm64
    Collecting package metadata (repodata.json): done
    Solving environment: done

    ## Package Plan ##

    environment location: /anvvsharma/agenticai/day01

    added / updated specs:
        - python=3.11


    The following NEW packages will be INSTALLED:

    bzip2              pkgs/main/osx-arm64::bzip2-1.0.8-h80987f9_6 
    ca-certificates    pkgs/main/osx-arm64::ca-certificates-2025.2.25-hca03da5_0 
    libffi             pkgs/main/osx-arm64::libffi-3.4.4-hca03da5_1 
    ncurses            pkgs/main/osx-arm64::ncurses-6.4-h313beb8_0 
    openssl            pkgs/main/osx-arm64::openssl-3.0.16-h02f6b3c_0 
    pip                pkgs/main/noarch::pip-25.1-pyhc872135_2 
    python             pkgs/main/osx-arm64::python-3.11.11-hb885b13_0 
    readline           pkgs/main/osx-arm64::readline-8.2-h1a28f6b_0 
    setuptools         pkgs/main/osx-arm64::setuptools-78.1.1-py311hca03da5_0 
    sqlite             pkgs/main/osx-arm64::sqlite-3.45.3-h80987f9_0 
    tk                 pkgs/main/osx-arm64::tk-8.6.14-h6ba3021_0 
    tzdata             pkgs/main/noarch::tzdata-2025b-h04d1e81_0 
    wheel              pkgs/main/osx-arm64::wheel-0.45.1-py311hca03da5_0 
    xz                 pkgs/main/osx-arm64::xz-5.6.4-h80987f9_1 
    zlib               pkgs/main/osx-arm64::zlib-1.2.13-h18a0788_1 


    Proceed ([y]/n)? y


    Downloading and Extracting Packages:

    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    #
    # To activate this environment, use
    #
    #     $ conda activate /anvvsharma/agenticai/day01
    #
    # To deactivate an active environment, use
    #
    #     $ conda deactivate

    (base) agenticai % 

### conda Command to activatae conda env
    
    $ conda activate /anvvsharma/agenticai/day01


### List conda Command to activatae conda env
    
    $ conda env list 

### Displays the list of conda environments:
                    * /anvvsharma/agenticai/day01
                    /Agentic-AI-2/day3-pydant/venv
base                /opt/miniconda3
agentic_2_base      /opt/miniconda3/envs/agentic_2_base


### Verify Python 3.11 env with version command
    $ python -V     
    $Python 3.11.11


### Verify Python 3.11 env with version command
    $ python -V     
    $Python 3.11.11

### Start Python interpreter (REPL) in Termina
    python

### Type this in the Python prompt
    print("Hello, World!")

### Exit the Python interpreter
    press quit() to exit        

### Instead create a hello.py file and run as bellow
    python hello.py


