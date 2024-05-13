# Initial values specified through a file
```bash
python main.py <file path>
```

The file must have 7 float values in a line, separated by commas

For example:

5,3,2.5,0.6,1,0.1,120

where each number corresponds to:

s0,i0,r0,beta,k,delta t, t final

The program allows the execution of multiple simulations with different values because it reads the values line by line. This means that, for example, if the file has 4 lines of values then 4 different simulations will be executed.

# Initial values specified through the command line
```bash
python main.py s0 i0 r0 beta k delta_t t_final
```