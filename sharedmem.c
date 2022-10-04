#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
/*
есть два подхода: shmget и mmap. Рассмотрим mmap, так как он более современный и гибкий,
но можно взглянуть на man shmget, если вы предпочитаете использовать инструменты старого стиля.
на mmap() функция может использоваться для выделения буферов памяти с настраиваемыми параметрами для управления доступом
и разрешениями, а также для их резервного копирования с хранилищем файловой системы, если это необходимо.

Cледующая функция создает буфер в памяти, которым процесс может поделиться со своими дочерними элементами:
*/
void* create_shared_memory(size_t size) { // size = 128
  // Наш буфер памяти будет доступен для чтения и записи:
  int protection = PROT_READ | PROT_WRITE;

  // Буфер будет общим (то есть другие процессы могут получить к нему доступ, но
  // анонимно (то есть сторонние процессы не могут получить для него адрес),
  // так что только этот процесс и его потомки смогут использовать его:
  int visibility = MAP_ANONYMOUS | MAP_SHARED;

   // Остальные параметры для `mmap ()` не важны для этого варианта использования,
   // но man-страница для `mmap` объясняет их назначение.
  return mmap(NULL, size, protection, visibility, 0, 0);
}
/*
Ниже приведен пример программы, которая использует функцию, описанную выше, чтобы выделить буфер.
Родительский процесс напишет сообщение, вилку, а затем дождется, пока его дочерний элемент изменит буфер.
Оба процесса могут читать и записывать общую память.
*/
#include <string.h>
#include <unistd.h>

int main() {

  char* parent_message = "hello";  // родительский процесс запишет это сообщение
  char* child_message = "goodbye"; // потом дочерний процесс запишет это сообщение следом
  void* shmem = create_shared_memory(128);
  memcpy(shmem, parent_message, sizeof(parent_message));

  int pid = fork();

  if (pid == 0) {
    printf("Child read: %s\n", shmem);
    memcpy(shmem, child_message, sizeof(child_message));
    printf("Child wrote: %s\n", shmem);

  } else {
    printf("Parent read: %s\n", shmem);
    sleep(1);
    printf("After 1s, parent read: %s\n", shmem);

  }
}