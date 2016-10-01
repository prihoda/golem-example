from golem.interfaces.facebook.responses import *
from urllib.parse import quote


def create_flows(version='default'):


    flows = {
        'default' : {
            'intent' : 'greeting',
            'states' : {
                'root' : {
                    'accept' : {
                        'template' : 'message',
                        'params' : {
                            'message' : 'Hi, welcome to IT support! :) Here\'s what you should do:',
                            'next' : 'find_button'
                        }
                    }
                },
                'find_button' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : TextMessage('Find a menu item or button which looks related to what you want to do', quick_replies=[
                                {'title':'OK'},
                                {'title':'I can\'t find one'}
                            ])
                        }
                    },
                    'accept' : {
                        'template' : 'input',
                        'params' : {
                            'entity' : 'button_answer',
                            'missing_message' : TextMessage('Choose one :)', quick_replies=[
                                {'title':'OK'},
                                {'title':'I can\'t find one'}
                            ]),
                            'next' : 'find_button_transition'
                        }
                    }
                },
                'find_button_transition' : {
                    'init' : {
                        'template' : 'value_transition',
                        'params' : {
                            'entity' : 'button_answer',
                            'transitions' : {
                                'ok' : 'click_it',
                                'cannot_find' : 'pick_random'
                            }
                        }
                    }
                }, 
                'click_it' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : 'Click it',
                            'next' : 'did_it_work'
                        }
                    }
                },
                'pick_random' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : TextMessage('Pick one at random', quick_replies=[
                                {'title':'OK'},
                                {'title':'I\'ve tried them all'}
                            ])
                        }
                    },
                    'accept' : {
                        'template' : 'input',
                        'params' : {
                            'entity' : 'button_answer',
                            'missing_message' : TextMessage('Choose one :)', quick_replies=[
                                {'title':'OK'},
                                {'title':'I\'ve tried them all'}
                            ]),
                            'next' : 'pick_random_transition'
                        }
                    }
                },
                'pick_random_transition' : {
                    'init' : {
                        'template' : 'value_transition',
                        'params' : {
                            'entity' : 'button_answer',
                            'transitions' : {
                                'ok' : 'click_it',
                                'tried_all' : 'google'
                            }
                        }
                    }
                }, 
                'google' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : ['Tell me the name of the program plus a few words related to what you want to do'],
                            #'next' : 'did_it_work' #Follow any instructions.
                        }
                    },
                    'accept' : action_search_google
                },
                'did_it_work' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : TextMessage('Did it work?', quick_replies=[
                                {'title':'Yes'},
                                {'title':'No'}
                            ])
                        }
                    },
                    'accept' : {
                        'template' : 'input',
                        'params' : {
                            'entity' : 'yes_no',
                            'missing_message' : 'Yes or no :)',
                            'next' : 'did_it_work_transition'
                        }
                    }
                },
                'did_it_work_transition' : {
                    'init' : {
                        'template' : 'value_transition',
                        'params' : {
                            'entity' : 'yes_no',
                            'transitions' : {
                                'yes' : 'done',
                                'no' : 'half_hour'
                            }
                        }
                    }
                }, 
                'half_hour' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : TextMessage('How long have you been trying this?', quick_replies=[
                                {'title':'5 mins'},
                                {'title':'10 mins'},
                                {'title':'half an hour'}
                            ])
                        }
                    },
                    'accept' : action_compare_time
                },
                'half_hour_transition' : {
                    'init' : {
                        'template' : 'value_transition',
                        'params' : {
                            'entity' : 'yes_no',
                            'transitions' : {
                                'yes' : 'ask_for_help',
                                'no' : 'find_button'
                            }
                        }
                    }
                }, 
                'ask_for_help' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : TextMessage('Ask someone for help or give up :(', buttons=[{'title':'Start again', 'payload':{'_state':'default.find_button'}}, {'title':'Show diagram', 'payload':{'intent':'about'}}])
                        }
                    }
                }, 
                'done' : {
                    'init' : {
                        'template' : 'message',
                        'params' : {
                            'message' : TextMessage('You\'re done! :)', buttons=[{'title':'Start again', 'payload':{'_state':'default.find_button'}}, {'title':'Show diagram', 'payload':{'intent':'about'}}])
                        }
                    }
                }, 
            }
        },
        'about' : {
            'states' : {
                'root' : {
                    'accept' : {
                        'template' : 'message',
                        'params' : {
                            'message' : AttachmentMessage(attachment_type='image', url='http://imgs.xkcd.com/comics/tech_support_cheat_sheet.png')
                        }
                    }
                }
            }
        }
    }
    return flows

def get_new_settings():
    menu = MenuSetting()
    #menu.create_element(type='postback', title='Tell me a joke', payload={'_state':'help.root'})
    #menu.create_element(type='postback', title='Help', payload={'_state':'help.root'})

    get_started = GetStartedSetting(payload={'_state':'default.first'})
    greeting = GreetingSetting(message="Hi {{user_first_name}}, I'm a bot designed to show how to use the Golem dialog manager :)")

    #return []
    return [menu, get_started, greeting]

def action_search_google(state):
    text = state.dialog.context.get('_message_text')
    message = TextMessage('Follow any instructions here:')
    message.create_button(title='Show Google results', url='http://lmgtfy.com/?q='+quote(text, safe=','))
    return message, 'did_it_work'

def action_compare_time(state):
    duration = state.dialog.context.get('duration', max_age=0)
    if not duration:
        return 'How long? Can you rephrase that? :)', None
    duration = float(duration)
    if duration >= 30:
        return None, 'ask_for_help'
    return None, 'find_button'