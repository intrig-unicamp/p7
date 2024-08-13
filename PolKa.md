# P7 + PolKa

## Requirements

- git 
- python3
- matplotlib
- networkX
- regex
- polka-routing

For the host

- hping3

## Download

```
git clone https://github.com/intrig-unicamp/p7.git
cd p7
git checkout polka
```

## Run P7 + Polka

### Prepare the Environment

It is recommended to have five open terminals.

1. Compile P4 code and run Tofino.
2. Load table information and configure ports.
3. Create the topology and generate files.
4. Host 1.
5. Host 2.

### Create the Topology and Generate Files

In **Terminal 3**, edit the *main.py* file with the topology, ports, and links information.

```
cd p7
nano main.p7
```

Generate the necessary files.
```
python main.py
```

Place the files in the correct directories.
```
./set_files.sh
```

### Compile P4 Code and Run Tofino Switch

In **Terminal 1**, compile the P4 code using the official P4 compiler.

If you are using P4 Studio, follow the next steps to compile the P4 codes:

```
cd bf-sde-9.13.2
```
```
. ../tools/set_sde.bash
```
Compile the custom P4 code (calculator use case):
```
../tools/p4_build.sh ~/p7/p4src/p7calc_mod.p4 
```
Compile P7's p4 code

```
../tools/p4_build.sh ~/p7/p4src/p7_polka.p4
```

Run the switch:

```
./run_switchd.sh -p p7_polka p7calc_mod -c ~/p7/p4src/multiprogram_custom_bfrt.conf
```

### Load the Tables and Set Ports

In **Terminal 2**:
```
cd bf-sde-9.13.2
```
```
. ../tools/set_sde.bash
```
Load table information:
```
bfshell -b ~p7/files/bfrt.py
```
Configure ports:
```
bfshell -f ~/p7/files/ports_config.txt -i
```

### Send Traffic

In **Terminal 4**, access host 1.

Configure the VLAN for P7 (change the interface name and the IP for your setup):

```
sudo ip link add link enp3s0f0 name enp3s0f0.1920 type vlan id 1920
```
```
sudo ifconfig enp3s0f0.1920 192.168.0.10 up
```

In **Terminal 5**, access host 2.

Configure the VLAN for P7 (change the interface name and the IP for your setup):
```
sudo ip link add link enp6s0f0 name enp6s0f0.1920 type vlan id 1920
```
```
sudo ifconfig enp6s0f0.1920 192.168.0.20 up

```

To validate the route that PolKa is using to reach the destination, you can use the TTL field.

The file [calculator](https://docs.google.com/spreadsheets/d/19dWWfbyr4qZv1m4FIzHOO8c77znra906RL7u58ySk80/edit?usp=sharing) shows the information of the tables and the result of the TTL when it reaches the destination.

For example, a ping from H1 to H2:

```
ping 192.168.0.20
```

The response should have a TTL of 103* (64 + 40).

\*The initial TTL is 64.

### Slice

To validate a specific route, use hpin3. Then, you can specify the TCP port

```
sudo hping3 192.168.0.20 -p 8080
```