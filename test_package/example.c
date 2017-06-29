#include <stdio.h>

#define UNW_LOCAL_ONLY
#include <libunwind.h>

int main() {
    unw_cursor_t cursor;
    unw_context_t context;
    
    unw_getcontext(&context);
    unw_init_local(&cursor, &context);
    unw_step(&cursor);
    
    char buf[256];
    unw_get_proc_name(&cursor, buf, sizeof(buf), NULL);
    
    puts(buf);
}
