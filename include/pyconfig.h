/* From /usr/include/python3.8 on WSL */

/* pyconfig.h */

/* Define if you have the readline library (-lreadline). */
#define HAVE_LIBREADLINE 1

/* Define if readline supports append_history */
#define HAVE_RL_APPEND_HISTORY 1

/* Define if you can turn off readline's signal handling. */
#define HAVE_RL_CATCH_SIGNAL 1

/* Define if you have readline 2.2 */
#define HAVE_RL_COMPLETION_APPEND_CHARACTER 1

/* Define if you have readline 4.0 */
#define HAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK 1

/* Define if you have readline 4.2 */
#define HAVE_RL_COMPLETION_MATCHES 1

/* Define if you have rl_completion_suppress_append */
#define HAVE_RL_COMPLETION_SUPPRESS_APPEND 1

/* Define if you have readline 4.0 */
#define HAVE_RL_PRE_INPUT_HOOK 1

/* Define if you have readline 4.0 */
#define HAVE_RL_RESIZE_TERMINAL 1


/* pythonrun.h */

/* Stuff with no proper home (yet) */
#ifndef Py_LIMITED_API
PyAPI_FUNC(char *) PyOS_Readline(FILE *, FILE *, const char *);
#endif
PyAPI_DATA(int) (*PyOS_InputHook)(void);
PyAPI_DATA(char) *(*PyOS_ReadlineFunctionPointer)(FILE *, FILE *, const char *);
#ifndef Py_LIMITED_API
PyAPI_DATA(PyThreadState*) _PyOS_ReadlineTState;
#endif

