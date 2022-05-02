t0 = {
    "source": "initial",
    "target": "s_standby"
}

t1 = {
    "source": "s_standby",
    "target": "s_working",
    "trigger": "start_work"
}

t2 = {
    "source": "s_working",
    "target": "s_standby",
    "trigger": "abort",
    "effect": "stop_timer('work_timer')"
}

t3 = {
    "source": "s_working",
    "target": "s_meeting_notify",
    "trigger": "work_timer"
}

t4 = {
    "source": "s_meeting_notify",
    "target": "s_working",
    "trigger": "dont_pause"
}

t5 = {
    "source": "s_meeting_notify",
    "target": "s_neg_connection",
    "trigger": "accept_pause",
    "effect": "start_timer('timeout', 60)"
}

t6 = {
    "source": "s_neg_connection",
    "target": "s_meeting",
    "trigger": "meeting_match"
}

t7 = {
    "source": "s_neg_connection",
    "target": "s_standby",
    "trigger": "timeout"
}

from stmpy import Machine, Driver
stm = Machine(transitions=[t0,t1,t2,t3,t4,t5,t6,t7], )
driver = Driver()
