#include <stdio.h>
#include <unistd.h>

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
    }
    else {
        /*
         * This block runs only in the parent process.
         * The parent can identify the child by the PID returned by fork().
         * The parent also has its own PID, which is different from the child.
         */
        printf("Parent process\n");
        printf("PID = %d\n", getpid());
        printf("Child PID = %d\n", pid);
    }

    /*
     * sleep(30) keeps both processes alive for 30 seconds so the user can
     * observe both the parent and child outputs before the program exits.
     * In real programs, the parent and child may perform different tasks
     * concurrently during this interval.
     */
    sleep(30);
    return 0;
}