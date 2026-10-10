#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

/*
 * This program demonstrates the behavior of fork() in Unix-like systems.
 *
 * fork() creates a new process by duplicating the current process.
 * After a successful fork:
 * - In the parent process, fork() returns the child process ID (PID).
 * - In the child process, fork() returns 0.
 *
 * Both parent and child continue executing from the next line after fork().
 * They each have their own memory space, but the child initially inherits
 * a copy of the parent's state.
 */

int main() {
    /*
     * pid stores the return value of fork().
     * If it is negative, the system call failed.
     * If it is zero, we are in the child process.
     * Otherwise, we are in the parent and pid contains the child's PID.
     */
    pid_t pid = fork();

    if (pid < 0) {
        /*
         * fork() failed. perror() prints a human-readable error message
         * describing the last system error that occurred.
         */
        perror("fork");
        return 1;
    }

    if (pid == 0) {
        /*
         * This block runs only in the child process.
         * The child process has a unique PID and a parent PID (PPID).
         * PPID is the PID of the parent process that created it.
         */
        printf("Child process\n");
        printf("PID = %d\n", getpid());
        printf("PPID = %d\n", getppid());

        sleep(2);
    }
    else {
        /*
         * The parent waits for the child to exit and inspects its exit status.
         * This prevents orphaned child processes and lets the parent report
         * whether the child ended normally or with an error.
         */
        int status;
        pid_t terminated_pid = waitpid(pid, &status, 0);

        if (terminated_pid == -1) {
            /*
             * waitpid() failed; report the OS-level error to the user.
             */
            perror("waitpid failed");
            return EXIT_FAILURE;
        }

        if (WIFEXITED(status)) {
            /*
             * The child exited normally. WEXITSTATUS() extracts its exit code.
             */
            int exit_code = WEXITSTATUS(status);
            printf("Child %d terminated normally with exit code: %d\n", terminated_pid, exit_code);
        } else {
            /*
             * The child did not terminate normally, such as by a signal.
             */
            printf("Child %d did not terminate normally.\n", terminated_pid);
        }

        /*
         * This block runs only in the parent process.
         * The parent can identify the child by the PID returned by fork().
         * The parent also has its own PID, which is different from the child.
         */
        
        /*
         * Delay the parent briefly so the child has time to complete its work
         * before the parent prints its own process information.
         */
        sleep(2);

        printf("Parent process\n");
        printf("PID = %d\n", getpid());
        printf("Child PID = %d\n", pid);
    }

    /*
     * Exit the process cleanly with a success status.
     */
    return 0;
}