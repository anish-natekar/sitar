import simpy
import random
import matplotlib.pyplot as plt
MIN_DELAY = 1
MAX_DELAY = 5
# load, store, rformat, branch
A = (0.15, 0.2, 0.4, 0.25)
B = (0.1, 0.1, 0.6, 0.2)
STAGES = [10, 10, 10, 10, 10]
INSTRUCTIONS = ("LOAD", "STORE", "RFORMAT", "BRANCH")
TOTAL_INSTRUCTIONS = 100
LOGS = (([],[],[]),([],[],[]))
def threeStaged(env, inst, IF_ID_3, EX_3, M_WB_3):
    global A, B, TOTAL_INSTRUCTIONS, INSTRUCTIONS, CTR_3
    with IF_ID_3.request() as req:
        yield req
        yield env.timeout(sum(STAGES[0:2]))
        IF_ID_3.release(req)
    with EX_3.request() as req:
        yield req
        yield env.timeout(STAGES[2])
        EX_3.release(req)
    if(inst != "BRANCH"):
        with M_WB_3.request() as req:
            yield req
            yield env.timeout(sum((STAGES[3:])))
            M_WB_3.release(req)
    CTR_3+=1
def fourStaged(env, inst, IF_4, ID_4, EX_4, M_WB_4):
    global A, B, TOTAL_INSTRUCTIONS, INSTRUCTIONS, CTR_4
    with IF_4.request() as req:
        yield req
        yield env.timeout(STAGES[0])
        IF_4.release(req)
    with ID_4.request() as req:
        yield req
        yield env.timeout(STAGES[1])
        ID_4.release(req)
    with EX_4.request() as req:
        yield req
        yield env.timeout(STAGES[2])
        EX_4.release(req)
    if(inst != "BRANCH"):
        with M_WB_4.request() as req:
            yield req
            yield env.timeout(sum((STAGES[3:])))
            M_WB_4.release(req)
    CTR_4+=1
def fiveStaged(env, inst, IF_5, ID_5, EX_5, M_5, WB_5):
    global A, B, TOTAL_INSTRUCTIONS, INSTRUCTIONS, CTR_5
    with IF_5.request() as req:
        yield req
        yield env.timeout(STAGES[0])
        IF_5.release(req)
    with ID_5.request() as req:
        yield req
        yield env.timeout(STAGES[1])
        ID_5.release(req)
    with EX_5.request() as req:
        yield req
        yield env.timeout(STAGES[2])
        EX_5.release(req)
    if(inst != "BRANCH"):
        if(inst != "RFORMAT"):
            with M_5.request() as req:
                yield req
                yield env.timeout(STAGES[3])
                M_5.release(req)
        elif(inst == "LOAD" or inst == "RFORMAT"):
            with WB_5.request() as req:
                yield req
                yield env.timeout(STAGES[4])
                WB_5.release(req)
    CTR_5+=1
def simulate(L):
    global CTR_3, CTR_4, CTR_5
    CTR_3 = 0
    CTR_4 = 0
    CTR_5 = 0
    env = simpy.Environment()
    # 5 stage
    IF_5 = simpy.Resource(env, capacity=1)
    ID_5 = simpy.Resource(env, capacity=1)
    EX_5 = simpy.Resource(env, capacity=1)
    M_5 = simpy.Resource(env, capacity=1)
    WB_5 = simpy.Resource(env, capacity=1)
    DONE_5 = env.event()
    # 4 stage
    IF_4 = simpy.Resource(env, capacity=1)
    ID_4 = simpy.Resource(env, capacity=1)
    EX_4 = simpy.Resource(env, capacity =1)
    M_WB_4 = simpy.Resource(env, capacity=1)
    DONE_4 = env.event()
    # 3 stage
    IF_ID_3 = simpy.Resource(env, capacity=1)
    EX_3 = simpy.Resource(env, capacity=1)
    M_WB_3 = simpy.Resource(env, capacity = 1)
    DONE_3 = env.event()
    env.process(checkCompletion_3(env, DONE_3, L))
    env.process(checkCompletion_4(env, DONE_4, L))
    env.process(checkCompletion_5(env, DONE_5, L))
    env.process(randomInstruction_3(env, L, IF_ID_3, EX_3, M_WB_3,
max(sum(STAGES[0:2]), STAGES[2], sum(STAGES[3:]))))
    env.process(randomInstruction_4(env, L, IF_4, ID_4, EX_4, M_WB_4,
max(STAGES[0], STAGES[1], STAGES[2], sum(STAGES[3:]))))
    env.process(randomInstruction_5(env, L, IF_5, ID_5, EX_5, M_5, WB_5,
max(STAGES)))
    env.run(DONE_5 & DONE_4 & DONE_3)
def randomInstruction_3(env, L, IF_ID_3, EX_3, M_WB_3, CLOCK):
    global TOTAL_INSTRUCTIONS, INSTRUCTIONS
    for i in range(TOTAL_INSTRUCTIONS):
        inst = int
        ran = random.random()
        for inst in range(4):
            if(ran <= sum(L[0:inst])):
                break
        env.process(threeStaged(env, INSTRUCTIONS[inst], IF_ID_3, EX_3,
M_WB_3))
        yield env.timeout(CLOCK)
def randomInstruction_4(env, L, IF_4, ID_4, EX_4, M_WB_4, CLOCK):
    global TOTAL_INSTRUCTIONS, INSTRUCTIONS
    for i in range(TOTAL_INSTRUCTIONS):
        inst = int
        ran = random.random()
        for inst in range(4):
            if(ran <= sum(L[0:inst])):
                break
        env.process(fourStaged(env, INSTRUCTIONS[inst], IF_4, ID_4, EX_4,
M_WB_4))
        yield env.timeout(CLOCK)
def randomInstruction_5(env, L, IF_5, ID_5, EX_5, M_5, WB_5, CLOCK):
    global TOTAL_INSTRUCTIONS, INSTRUCTIONS
    for i in range(TOTAL_INSTRUCTIONS):
        inst = int
        ran = random.random()
        for inst in range(4):
            if(ran <= sum(L[0:inst])):
                break
        env.process(fiveStaged(env, INSTRUCTIONS[inst], IF_5, ID_5, EX_5,
M_5, WB_5))
        yield env.timeout(CLOCK)
def checkCompletion_3(env, DONE_3, L):
    global CTR_3, TOTAL_INSTRUCTIONS
    while(CTR_3<TOTAL_INSTRUCTIONS):
        yield env.timeout(10)
    print("3 stage process ended at", env.now)
    if L == A:
        LOGS[0][0].append(env.now)
    elif L == B:
        LOGS[1][0].append(env.now)
    DONE_3.succeed()
def checkCompletion_4(env, DONE_4, L):
    global CTR_4, TOTAL_INSTRUCTIONS
    while(CTR_4<TOTAL_INSTRUCTIONS):
        yield env.timeout(10)
    print("4 stage process ended at", env.now)
    if L == A:
        LOGS[0][1].append(env.now)
    elif L == B:
        LOGS[1][1].append(env.now)
    DONE_4.succeed()
def checkCompletion_5(env,DONE_5, L):
    global CTR_5, TOTAL_INSTRUCTIONS
    while(CTR_5<TOTAL_INSTRUCTIONS):
        yield env.timeout(10)
    print("5 stage process ended at", env.now)
    if L == A:
        LOGS[0][2].append(env.now)
    elif L == B:
        LOGS[1][2].append(env.now)
    DONE_5.succeed()
for STAGES[0] in range(10, 51, 10):
    for STAGES[1] in range(10, 51, 10):
        for STAGES[2] in range(10, 51, 10):
            for STAGES[3] in range(10, 51, 10):
                for STAGES[4] in range(10, 51, 10):
                    simulate(A)
                    simulate(B)
plt.figure(figsize=(25,5))
plt.plot(range(1,3126), LOGS[0][0])
plt.title("3 staged with Instruction set 1")
plt.show()
input("Press any key to continue")
plt.figure(figsize=(25,5))
plt.plot(range(1,3126), LOGS[0][1])
plt.title("4 staged with Instruction set 1")
plt.show()
input("Press any key to continue")
plt.figure(figsize=(25,5))
plt.plot(range(1,3126), LOGS[0][2])
plt.title("5 staged with Instruction set 1")
plt.show()
input("Press any key to continue")
plt.figure(figsize=(25,5))
plt.plot(range(1,3126), LOGS[1][0])
plt.title("3 staged with Instruction set 2")
plt.show()
input("Press any key to continue")
plt.figure(figsize=(25,5))
plt.plot(range(1,3126), LOGS[1][1])
plt.title("4 staged with Instruction set 2")
plt.show()
input("Press any key to continue")
plt.figure(figsize=(25,5))
plt.plot(range(1,3126), LOGS[1][2])
plt.title("5 staged with Instruction set 2")
plt.show()