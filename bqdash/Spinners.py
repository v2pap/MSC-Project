from ipywidgets import HTML,Output,VBox,HBox,Label



class Spinner(HBox):

    def __init__(self, loading_text, string, spinner_default_margin, *args, **kwargs):
        self.loading_text = loading_text
        self.spinner = HTML(string)
        self.spinner.layout.margin = spinner_default_margin
        if 'layout' not in kwargs:
            self.layout = layout={'overflow':'hidden'}
        super().__init__(children=[self.spinner, self.loading_text], *args, **kwargs)

    def update_loading_text(self,new_text):
        self.loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=new_text))
        self.children=[self.spinner, self.loading_text]


class TripleSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#ff6f00','#7b1af9','#FFFFFF'], *args, **kwargs):

        if len(colors) == 1:
            colors.append('#7b1af9')
            colors.append('#FFFFFF')
        elif len(colors) == 2:
            colors.append('#FFFFFF')
        elif len(colors) ==0:
            colors=['#ff6f00','#7b1af9','#FFFFFF']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))
        string =  '''<style>
                                    #loader {
                                        display: block;
                                        position: relative;
                                        width: 25px;
                                        height: 25px;
                                        border-radius: 50%;
                                        border: 2px solid transparent;
                                        border-top-color: {outside};
                                        animation: spin 2s linear infinite;
                                        z-index: 1001;
                                    }

                                    #loader:after {
                                        content: "";
                                        position: absolute;
                                        top: 2.5px;
                                        left: 2.5px;
                                        right: 2.5px;
                                        bottom: 2.5px;
                                        border-radius: 50%;
                                        border: 2px solid transparent;
                                        border-top-color: {middle};
                                        animation: spin 1.5s linear infinite;
                                    }

                                    #loader:before {
                                        content: "";
                                        position: absolute;
                                        top: 7.5px;
                                        left: 7.5px;
                                        right: 7.5px;
                                        bottom: 7.5px;
                                        border-radius: 50%;
                                        border: 2px solid transparent;
                                        border-top-color: {inner};
                                        animation: spin 2s linear infinite;
                                    }



                                    @keyframes spin {
                                      0% { transform: rotate(0deg); }
                                      100% { transform: rotate(360deg); }
                                    }
                            </style>
                            <div id="loader"></div>'''.replace('{outside}',colors[0]).replace('{middle}',colors[1]).replace('{inner}',colors[2])
        margin = '15px 0px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)

class ReverseSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''

    def __init__(self, text='Loading...', colors=['#1976d2','#03a9f4'], *args, **kwargs):

        if len(colors) == 1:
            colors.append('#03a9f4')
        elif len(colors) ==0:
            colors=['#1976d2','#03a9f4']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))
        string =  '''<style>
                                  .reverse-spinner {
                                            position: relative;
                                            height: 25px;
                                            width: 25px;
                                            border: 2px solid transparent;
                                            border-top-color: {outside};
                                            border-left-color: {outside};
                                            border-radius: 50%;
                                            -webkit-animation: spin 1.5s linear infinite;
                                            animation: spin 1.5s linear infinite;
                                          }

                                  .reverse-spinner::before {
                                    position: absolute;
                                    top: 5px;
                                    left: 5px;
                                    right: 5px;
                                    bottom: 5px;
                                    content: "";
                                    border:2px solid transparent;
                                    border-top-color: {inside};
                                    border-left-color: {inside};
                                    border-radius: 50%;
                                    -webkit-animation: spinBack 1s linear infinite;
                                    animation: spinBack 1s linear infinite;
                                  }

                                  @-webkit-keyframes spin {
                                      from {
                                        -webkit-transform: rotate(0deg);
                                        transform: rotate(0deg);
                                      }
                                      to {
                                        -webkit-transform: rotate(360deg);
                                        transform: rotate(360deg);
                                      }
                                  }

                              @keyframes spin {
                                  from {
                                    -webkit-transform: rotate(0deg);
                                    transform: rotate(0deg);
                                  }
                                  to {
                                    -webkit-transform: rotate(360deg);
                                    transform: rotate(360deg);
                                  }
                              }


                              @-webkit-keyframes spinBack {
                                  from {
                                      -webkit-transform: rotate(0deg);
                                      transform: rotate(0deg);
                                }
                                to {
                                      -webkit-transform: rotate(-720deg);
                                      transform: rotate(-720deg);
                                }
                              }

                              @keyframes spinBack {
                                from {
                                      -webkit-transform: rotate(0deg);
                                      transform: rotate(0deg);
                                }
                                to {
                                      -webkit-transform: rotate(-720deg);
                                      transform: rotate(-720deg);
                                }
                              }
                        </style>

                        <div class="reverse-spinner"></div>'''.replace('{outside}',colors[0]).replace('{inside}',colors[1])
        margin = '15px 0px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)


class CircleSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#03A9F4'], *args, **kwargs):

        if len(colors) ==0:
            colors=['#03A9F4']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))
        string =  '''<style>
                            .bt-spinner {
                                width: 25px;
                                height: 25px;
                                border-radius: 50%;
                                background-color: transparent;
                                border: 2px solid #222;
                                border-top: 2px solid {outside};
                                -webkit-animation: 1s spin linear infinite;
                                animation: 1s spin linear infinite;
                            }

                            @-webkit-keyframes spin {
                                from {
                                    -webkit-transform: rotate(0deg);
                                    transform: rotate(0deg);
                                }
                                to {
                                    -webkit-transform: rotate(360deg);
                                    transform: rotate(360deg);
                                }
                            }

                            @keyframes spin {
                                from {
                                    -webkit-transform: rotate(0deg);
                                    transform: rotate(0deg);
                                }
                                to {
                                    -webkit-transform: rotate(360deg);
                                    transform: rotate(360deg);
                                }
                            }
                            </style>


                            <div class="bt-spinner"></div>'''.replace('{outside}',colors[0])
        margin = '15px 0px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)


#                        .circle-loader {
#                                 position: relative;
#                                 height: 10px;
#                                 width: 10px;

#                                 }

class TriforceSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#cccc00'], *args, **kwargs):

        if len(colors) == 0:
            colors=['#cccc00']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))

        string =  '''<style>
                     .triforce-container {
                        width: 15px;
                        height: 15px;
                        position: relative;

                      }
                      .triforce,
                      .triforce::before,
                      .triforce::after {
                        width: 0;
                        height: 0;
                        border-left: 5px solid transparent;
                        border-right: 5px solid transparent;
                        border-bottom: 10px solid #ceb502;
                        position: relative;
                        -webkit-animation: 3s triforce linear infinite 2s both;
                                animation: 3s triforce linear infinite 2s both;
                        top: 10px;
                      }

                      .triforce::before,
                      .triforce::after {
                        content: "";
                        position: absolute;
                      }

                      .triforce::before {
                        left: 5px;
                        top: 0;
                        -webkit-animation-delay: 1s;
                                animation-delay: 1s;
                      }

                      .triforce::after {
                        top: -10px;
                        -webkit-animation-delay: 0s;
                                animation-delay: 0s;
                      }

                      @-webkit-keyframes triforce {
                          0%, 40%, 100% {
                            border-bottom-color: {outside};
                          }
                          40% {
                            border-bottom-color: #000000;
                          }
                        }

                      @keyframes triforce {
                          0%, 40%, 100% {
                            border-bottom-color: {outside};
                          }
                          40% {
                            border-bottom-color: #000000;
                          }
                        }
                    </style>


                    <div class="triforce-container">
                      <div class="triforce"></div>
                    </div>'''.replace('{outside}',colors[0])
        margin = '15px 0px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)
#rgb(206, 181, 2);
#rgba(206, 181, 2, 0)
class MultiSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#ff5722'], *args, **kwargs):


        if len(colors) ==0:
            colors=['#ff5722']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))

        string =  '''<style>
                      .multi-spinner-container {
                      width: 50px;
                      height: 50px;
                      position: relative;
                      overflow: hidden;
                    }

                    .multi-spinner {
                      position: absolute;
                      width: calc(100% - 9.9px);
                      height: calc(100% - 9.9px);
                      border: 1px solid transparent;
                      border-top-color: {outside};
                      border-radius: 50%;
                      -webkit-animation: spin 5s cubic-bezier(0.17, 0.49, 0.96, 0.76) infinite;
                      animation: spin 5s cubic-bezier(0.17, 0.49, 0.96, 0.76) infinite;
                    }


                    @-webkit-keyframes spin {
                        from {
                            -webkit-transform: rotate(0deg);
                             transform: rotate(0deg);
                        }
                        to {
                            -webkit-transform: rotate(360deg);
                            transform: rotate(360deg);
                        }
                    }


                    @keyframes spin {
                        from {
                            -webkit-transform: rotate(0deg);
                            transform: rotate(0deg);
                        }
                        to {
                            -webkit-transform: rotate(360deg);
                            transform: rotate(360deg);
                        }
                    }
                    </style>


                    <div class="multi-spinner-container">
                        <div class="multi-spinner">
                            <div class="multi-spinner">
                                <div class="multi-spinner">
                                    <div class="multi-spinner">
                                        <div class="multi-spinner">
                                            <div class="multi-spinner"> </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>


                    '''.replace('{outside}',colors[0])
        margin = '15px 0px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)

class CentreSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#9C27B0','#9C27B0'], *args, **kwargs):

        if len(colors) == 1:
            colors.append('#9C27B0')
        elif len(colors) ==0:
            colors=['#9C27B0','#9C27B0']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))

        string =  '''<style>
                        .hm-spinner{
                          height: 30px;
                          width: 30px;
                          border: 3px solid transparent;
                          border-top-color: {outside};
                          border-bottom-color: {outside};
                          border-radius: 50%;
                          position: relative;
                          -webkit-animation: spin 2.5s linear infinite;
                                  animation: spin 2.5s linear infinite;
                        }

                        .hm-spinner::before{
                          content: "";
                          position: absolute;
                          top: 5px;
                          right: 5px;
                          bottom: 5px;
                          left: 5px;
                          border: 3px solid transparent;
                          border-top-color: {inside};
                          border-bottom-color: {inside};
                          border-radius: 50%;
                          -webkit-animation: spin 2.5s linear infinite;
                          animation: spin 2.5s linear infinite;
                        }

                        @-webkit-keyframes spin {
                            from {
                              -webkit-transform: rotate(0deg);
                              transform: rotate(0deg);
                            }
                            to {
                              -webkit-transform: rotate(360deg);
                              transform: rotate(360deg);
                            }
                        }

                        @keyframes spin {
                            from {
                              -webkit-transform: rotate(0deg);
                              transform: rotate(0deg);
                            }
                            to {
                              -webkit-transform: rotate(360deg);
                              transform: rotate(360deg);
                            }
                        }
                        </style>


                        <div class="hm-spinner"></div>

                    '''.replace('{outside}',colors[0]).replace('{inside}',colors[1])
        margin = '15px 0px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)

class SunSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#f44e03'], *args, **kwargs):

        if len(colors) == 0:
            colors=['#f44e03']


        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))

        string =  '''<style>

                          .ml-loader {
                                        -webkit-transform:scale(0.5);
                                        -webkit-transform-origin:top left;
                                        -moz-transform:scale(0.5);
                                        -moz-transform-origin:top left;
                                        -ms-transform:scale(0.5);
                                        -ms-transform-origin:top left;
                                        -o-transform:scale(0.5);
                                        -o-transform-origin:top left;
                                        transform:scale(0.5);
                                        transform-origin:top left;
                                    }

                          .ml-loader div {
                            -webkit-transform-origin: 32px 32px;
                                -ms-transform-origin: 32px 32px;
                                    transform-origin: 32px 32px;
                            -webkit-animation: 1.2s opaque ease-in-out infinite both;
                                    animation: 1.2s opaque ease-in-out infinite both;
                          }

                          .ml-loader div::after {
                            content: "";
                            display: block;
                            position: absolute;
                            top: 5px;
                            left: 30px;
                            width: 3px;
                            height: 15px;
                            border-radius: 3px;
                            background-color: {outside};
                          }

                          .ml-loader div:nth-child(1) {
                            -webkit-transform: rotate(0);
                                -ms-transform: rotate(0);
                                    transform: rotate(0);
                          }
                          .ml-loader div:nth-child(2) {
                            -webkit-transform: rotate(30deg);
                                -ms-transform: rotate(30deg);
                                    transform: rotate(30deg);
                            -webkit-animation-delay: 0.1s;
                                    animation-delay: 0.1s;
                          }
                          .ml-loader div:nth-child(3) {
                            -webkit-transform: rotate(60deg);
                                -ms-transform: rotate(60deg);
                                    transform: rotate(60deg);
                            -webkit-animation-delay: 0.2s;
                                    animation-delay: 0.2s;
                          }
                          .ml-loader div:nth-child(4) {
                            -webkit-transform: rotate(90deg);
                                -ms-transform: rotate(90deg);
                                    transform: rotate(90deg);
                            -webkit-animation-delay: 0.3s;
                                    animation-delay: 0.3s;
                          }
                          .ml-loader div:nth-child(5) {
                            -webkit-transform: rotate(120deg);
                                -ms-transform: rotate(120deg);
                                    transform: rotate(120deg);
                            -webkit-animation-delay: 0.4s;
                                    animation-delay: 0.4s;
                          }
                          .ml-loader div:nth-child(6) {
                            -webkit-transform: rotate(150deg);
                                -ms-transform: rotate(150deg);
                                    transform: rotate(150deg);
                            -webkit-animation-delay: 0.5s;
                                    animation-delay: 0.5s;
                          }
                          .ml-loader div:nth-child(7) {
                            -webkit-transform: rotate(180deg);
                                -ms-transform: rotate(180deg);
                                    transform: rotate(180deg);
                            -webkit-animation-delay: 0.6s;
                                    animation-delay: 0.6s;
                          }
                          .ml-loader div:nth-child(8) {
                            -webkit-transform: rotate(210deg);
                                -ms-transform: rotate(210deg);
                                    transform: rotate(210deg);
                            -webkit-animation-delay: 0.7s;
                                    animation-delay: 0.7s;
                          }
                          .ml-loader div:nth-child(9) {
                            -webkit-transform: rotate(240deg);
                                -ms-transform: rotate(240deg);
                                    transform: rotate(240deg);
                            -webkit-animation-delay: 0.8s;
                                    animation-delay: 0.8s;
                          }
                          .ml-loader div:nth-child(10) {
                            -webkit-transform: rotate(270deg);
                                -ms-transform: rotate(270deg);
                                    transform: rotate(270deg);
                            -webkit-animation-delay: 0.9s;
                                    animation-delay: 0.9s;
                          }
                          .ml-loader div:nth-child(11) {
                            -webkit-transform: rotate(300deg);
                                -ms-transform: rotate(300deg);
                                    transform: rotate(300deg);
                            -webkit-animation-delay: 1s;
                                    animation-delay: 1s;
                          }
                          .ml-loader div:nth-child(12) {
                            -webkit-transform: rotate(330deg);
                                -ms-transform: rotate(330deg);
                                    transform: rotate(330deg);
                            -webkit-animation-delay: 1.1s;
                                    animation-delay: 1.1s;
                          }
                          .ml-loader div:nth-child(13) {
                            -webkit-transform: rotate(360deg);
                                -ms-transform: rotate(360deg);
                                    transform: rotate(360deg);
                            -webkit-animation-delay: 1.2s;
                                    animation-delay: 1.2s;
                          }

                          @-webkit-keyframes opaque {
                              0%, 40%, 100% {
                                opacity: 0.1;
                              }
                              40% {
                                opacity: 1;
                              }
                          }

                          @keyframes opaque {
                              0%, 40%, 100% {
                                opacity: 0.1;
                              }
                              40% {
                                opacity: 1;
                              }
                          }

                        </style>

                        <div class="ml-loader">
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                        </div>

                    '''.replace('{outside}',colors[0])
        margin = '15px 15px 0px 0px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)

class DotSpinner(Spinner):
    '''
    Displays a loading spinner and text to describe action.

    Parameters
    ----------
    text(string): text to display for describing action

    colors(list):list of colours for the spinner

    '''
    def __init__(self, text='Loading...', colors=['#03A9F4'], *args, **kwargs):

        if len(colors) == 0:
            colors=['#03A9F4']

        loading_text = HTML('<h2 style="color: lightgrey; font-weight: bold;font-size=8;">{text}</h2>'.format(text=text))
        string =  '''<style>

                                .circle-loader {
                                        -webkit-transform:scale(0.5);
                                        -webkit-transform-origin:top left;
                                        -moz-transform:scale(0.5);
                                        -moz-transform-origin:top left;
                                        -ms-transform:scale(0.5);
                                        -ms-transform-origin:top left;
                                        -o-transform:scale(0.5);
                                        -o-transform-origin:top left;
                                        transform:scale(0.5);
                                        transform-origin:top left;
                                    }

                                .circle-loader div {
                                    height: 10px;
                                    width: 10px;
                                    background-color: {outside};
                                    border-radius: 50%;
                                    position: absolute;
                                    -webkit-animation: 1.3s opaque ease-in-out infinite both;
                                    animation: 1.3s opaque ease-in-out infinite both;
                                }


                                .circle-loader > div:nth-child(1) {
                                    top: -25px;
                                    left: 0;
                                }

                                .circle-loader > div:nth-child(2) {
                                    top: -17px;
                                    left: 17px;
                                    -webkit-animation-delay: .15s;
                                    animation-delay: .15s;
                                }

                                .circle-loader > div:nth-child(3) {
                                    top: 0;
                                    left: 25px;
                                    -webkit-animation-delay: 0.3s;
                                    animation-delay: 0.3s;
                                }

                                .circle-loader > div:nth-child(4) {
                                    top: 17px;
                                    left: 17px;
                                    -webkit-animation-delay: 0.45s;
                                    animation-delay: 0.45s;
                                }

                                .circle-loader > div:nth-child(5) {
                                    top: 25px;
                                    left: 0;
                                    -webkit-animation-delay: 0.6s;
                                    animation-delay: 0.6s;
                                }

                                .circle-loader > div:nth-child(6) {
                                    top: 17px;
                                    left: -17px;
                                    -webkit-animation-delay: 0.75s;
                                    animation-delay: 0.75s;
                                }

                                .circle-loader > div:nth-child(7) {
                                    top: 0;
                                    left: -25px;
                                    -webkit-animation-delay: .9s;
                                    animation-delay: .9s;
                                }

                                .circle-loader > div:nth-child(8) {
                                    top: -17px;
                                    left: -17px;
                                    -webkit-animation-delay: 1.05s;
                                    animation-delay: 1.05s;
                                }



                                @-webkit-keyframes opaque {
                                    0%, 40%, 100% {
                                      opacity: 0.1;
                                    }
                                    40% {
                                      opacity: 1;
                                    }
                                }

                                @keyframes opaque {
                                    0%, 40%, 100% {
                                      opacity: 0.1;
                                    }
                                    40% {
                                      opacity: 1;
                                    }
                                }
                                </style>


                                <div class="circle-loader">
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                    <div></div>

                                </div>'''.replace('{outside}',colors[0])
        margin = '25px 15px 0px 20px'
        super().__init__(loading_text=loading_text, string=string,spinner_default_margin=margin, *args, **kwargs)
