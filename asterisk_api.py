#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
import sys
import argparse

from asterisk import manager


class SETTINGS:
    AMI_USER = ''
    AMI_PASSWORD = ''
    AMI_SERVER = '127.0.0.1'


def connection_ami(user, pasw, host):
    """
    подключение к asterisk по протоколу ami
    """
    ami = manager.Manager()
    try:
        ami.connect(host)
        ami.login(username=user, secret=pasw)
        return ami
    except:
        return False


def originate(ami, number, context_call, context_answer, **kwargs):
    """
    совершение звонка и отправка dtmf сигнала
    """
    ami.originate(
            channel='LOCAL/%s@%s' % (number, context_call),
            exten='s',
            context=context_answer,
            priority=1,
            async=False,
            variables=kwargs)


def call(number, voice, reportfile):
    conn = connection_ami(SETTINGS.AMI_USER,
                          SETTINGS.AMI_PASSWORD,
                          SETTINGS.AMI_SERVER)
    if not conn:
        print('erros')

    parametrs = {
        'PHONE': number,
        'REPORTFILE': reportfile,
        'VOICE': voice}

    originate(conn, number,
              'callback_dial', 'callback_answer', **parametrs)
    conn.close()
