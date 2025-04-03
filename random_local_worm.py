import random
import matplotlib.pyplot as plt
import numpy as np


runs = 3
OMEGA = 100000
Total_vulnerable_ip = 1000
total_simulation_steps = 10000
SCAN_RATE = 3


def initialize_ip_address_state():
    ip_addr_space = ['immune' for i in range(OMEGA+1)]
    for i in range(int(1000/10)):
        for j in range(1, 11):
            ip_addr_space[j + (i * 1000)] = 'vulnerable'
    return ip_addr_space


def get_local_ips(ip_addr_state):
    local_ips = []
    for ip in range(OMEGA):
        if ip_addr_state[ip] == 'infected':
            for _ in range(SCAN_RATE):
                if ip <= 10:
                    rule = np.random.choice(['rule1', 'rule2'], 1, p=[0.8, 0.2])
                    if rule == 'rule1':
                        infect_ip = random.sample(range(1, ip + 1 + 10), 1)
                    elif rule == 'rule2':
                        infect_ip = random.sample(range(1, OMEGA + 1), 1)
                elif ip >= (OMEGA - 10):
                    rule = np.random.choice(['rule1', 'rule2'], 1, p=[0.8, 0.2])
                    if rule == 'rule1':
                        infect_ip = random.sample(range(ip - 10, OMEGA + 1), 1)
                    elif rule == 'rule2':
                        infect_ip = random.sample(range(1, OMEGA + 1), 1)
                else:
                    rule = np.random.choice(['rule1', 'rule2'], 1, p=[0.8, 0.2])
                    if rule == 'rule1':
                        infect_ip = random.sample(range(ip - 10, ip + 1 + 10), 1)
                    elif rule == 'rule2':
                        infect_ip = random.sample(range(1, OMEGA + 1), 1)
                local_ips.append(infect_ip[0])
    return local_ips


def worm_propagation(ip_addr_state, method):
    infected_ip_count_discrete = []
    num_of_infected_ip = 1
    for tick in range(total_simulation_steps):
        num_of_ips_to_scan = num_of_infected_ip * SCAN_RATE
        if method == 'random_scan':
            infected_ips = random.sample(range(1, OMEGA + 1), num_of_ips_to_scan)
        elif method == 'local_preference':
            infected_ips = get_local_ips(ip_addr_state)
        for ip in infected_ips:
            if ip_addr_state[ip] == 'vulnerable':
                ip_addr_state[ip] = 'infected'
                num_of_infected_ip += 1
                if num_of_infected_ip == Total_vulnerable_ip:
                    break

        if (tick + 1) % 100 == 0:
            print("Time steps: {0} ---- IPs_infected: {1}".format(tick + 1, num_of_infected_ip))
        infected_ip_count_discrete.append(num_of_infected_ip)
        if num_of_infected_ip == Total_vulnerable_ip:
            print("Time steps: {0} ---- IPs_infected: {1}. \nAll IPs infected!!!".format(tick + 1,
                                                                                              num_of_infected_ip))
            break
    return infected_ip_count_discrete


def plot_simulation(count, run):
    plt.plot(count, "-", label="Run #{}".format(run + 1))


def worm_propagation_simulation(method, plot=False):
    for run in range(runs):
        print("\n ****** {} Scan worm propagation: Run{}******".format(method, run+1))
        ip_addr_state = initialize_ip_address_state()
        # print([i for i, x in enumerate(ip_addr_state) if x == 'immune'])
        ip_addr_state[1001] = 'infected'
        infected_ip_count_discrete = worm_propagation(ip_addr_state, method)
        if plot:
            plot_simulation(infected_ip_count_discrete, run)
    if plot:
        plt.xlabel("Time tick")
        plt.ylabel("Number of infected computers")
        plt.title("{}: 3 Simulation Runs of Worm Propagation".format(method))
        plt.legend()
        plt.show()


def main():
    random.seed(1)
    methods = ['local_preference']
    for method in methods:
        worm_propagation_simulation(method, plot=False)


main()
