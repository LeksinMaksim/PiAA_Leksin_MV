#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int row;
    int col;
    int size;
} SquareInfo;

int gridSize;
int minSquareCount;
SquareInfo* optimalSolution;
int** grid;
int backtrackCalls = 0;
int squaresPlaced = 0;
int squaresRemoved = 0;

void printGrid() {
    printf("\n═════ Текущее состояние сетки %d×%d ═════\n", gridSize, gridSize);
    printf("    ");
    for (int j = 0; j < gridSize; j++) {
        printf("%2d ", j + 1);
    }
    printf("\n    ");
    for (int j = 0; j < gridSize; j++) {
        printf("───");
    }
    printf("\n");
    
    for (int i = 0; i < gridSize; i++) {
        printf("%2d │ ", i + 1);
        for (int j = 0; j < gridSize; j++) {
            if (grid[i][j] == 0) {
                printf(" · ");
            } else {
                printf("%2d ", grid[i][j]);
            }
        }
        printf("\n");
    }
    printf("════════════════════════════════════\n");
}

bool canPlaceSquare(int row, int col, int size) {
    printf("Проверка возможности размещения квадрата размера %d в позиции (%d, %d)\n", 
            size, row + 1, col + 1);
    
    if (row + size > gridSize || col + size > gridSize) {
        printf("  Квадрат выходит за границы сетки\n");
        return false;
    }
    
    for (int i = row; i < row + size; i++) {
        for (int j = col; j < col + size; j++) {
            if (grid[i][j] != 0) {
                printf("  Ячейка (%d, %d) уже занята квадратом #%d\n", i + 1, j + 1, grid[i][j]);
                return false;
            }
        }
    }
    
    printf("  Квадрат можно разместить\n");
    return true;
}

void markArea(int row, int col, int size, int value) {
    if (value > 0) {
        printf("Размещение квадрата #%d размера %d в позиции (%d, %d)\n", 
               value, size, row + 1, col + 1);
        squaresPlaced++;
    } else {
        printf("Удаление квадрата из позиции (%d, %d) размера %d\n", 
               row + 1, col + 1, size);
        squaresRemoved++;
    }
    
    for (int i = row; i < row + size; i++) {
        for (int j = col; j < col + size; j++) {
            grid[i][j] = value;
        }
    }
}

void saveSolution(int count, SquareInfo* squares) {
    printf("\nНАЙДЕНО НОВОЕ ОПТИМАЛЬНОЕ РЕШЕНИЕ: %d квадратов (ранее было: %d)\n", 
           count, minSquareCount);
    
    minSquareCount = count;
    
    printf("Решение содержит следующие квадраты:\n");
    for (int i = 0; i < count; i++) {
        optimalSolution[i].row = squares[i].row + 1;
        optimalSolution[i].col = squares[i].col + 1;
        optimalSolution[i].size = squares[i].size;
        
        printf("  Квадрат #%d: позиция (%d, %d), размер %d\n", 
               i + 1, optimalSolution[i].row, optimalSolution[i].col, optimalSolution[i].size);
    }
    printf("\n");
}

bool findFirstEmptyCell(int* outRow, int* outCol) {
    for (int row = 0; row < gridSize; row++) {
        for (int col = 0; col < gridSize; col++) {
            if (grid[row][col] == 0) {
                *outRow = row;
                *outCol = col;
                printf("Найдена первая пустая ячейка в позиции (%d, %d)\n", row + 1, col + 1);
                return true;
            }
        }
    }
    printf("Пустых ячеек не найдено. Все заполнено!\n");
    return false;
}

bool handleSpecialCases() {
    printf("\nПроверка особых случаев для gridSize = %d\n", gridSize);
    
    if (gridSize % 2 == 0) {
        int half = gridSize / 2;
        printf("Особый случай: gridSize делится на 2. Можно покрыть 4 квадратами размера %d\n", half);
        
        SquareInfo squares[4] = {
            {0, 0, half},
            {half, 0, half},
            {0, half, half},
            {half, half, half}
        };
        saveSolution(4, squares);
        return true;
    } else if (gridSize % 3 == 0) {
        int third = gridSize / 3;
        printf("Особый случай: gridSize делится на 3. Можно покрыть 6 квадратами\n");
        
        SquareInfo squares[6] = {
            {0, 0, 2 * third},
            {0, 2 * third, third},
            {third, 2 * third, third},
            {2 * third, 0, third},
            {2 * third, third, third},
            {2 * third, 2 * third, third}
        };
        saveSolution(6, squares);
        return true;
    } else if (gridSize % 5 == 0) {
        int fifth = gridSize / 5;
        printf("Особый случай: gridSize делится на 5. Можно покрыть 8 квадратами\n");
        
        SquareInfo squares[8] = {
            {0, 0, 3 * fifth},
            {3 * fifth, 0, 2 * fifth},
            {3 * fifth, 2 * fifth, 2 * fifth},
            {0, 3 * fifth, 2 * fifth},
            {2 * fifth, 3 * fifth, fifth},
            {2 * fifth, 4 * fifth, fifth},
            {3 * fifth, 4 * fifth, fifth},
            {4 * fifth, 4 * fifth, fifth}
        };
        saveSolution(8, squares);
        return true;
    }
    
    printf("Для N = %d не найдено особых случаев. Применяем общий алгоритм\n", gridSize);
    return false;
}

int min3(int a, int b, int c) {
    int min = a;
    if (b < min) min = b;
    if (c < min) min = c;
    return min;
}

void backtrack(int currentCount, SquareInfo* squares, int remainingArea) {
    backtrackCalls++;
    
    printf("\n----- Вызов backtrack #%d -----\n", backtrackCalls);
    printf("Текущее количество квадратов: %d, Оптимальное: %d, Оставшаяся площадь: %d\n", 
           currentCount, minSquareCount, remainingArea);
    
    if (currentCount >= minSquareCount) {
        printf("Отсечение ветви: текущее количество квадратов >= минимальное (%d >= %d)\n", 
               currentCount, minSquareCount);
        return;
    }
    
    int row, col;
    if (findFirstEmptyCell(&row, &col)) {
        int maxSize = min3(gridSize - row, gridSize - col, (gridSize + 1) / 2);
        printf("Максимально возможный размер квадрата для позиции (%d, %d): %d\n", 
               row + 1, col + 1, maxSize);
        
        for (int size = maxSize; size >= 1; size--) {
            printf("\nПробуем поставить квадрат размера %d в позицию (%d, %d)...\n", 
                   size, row + 1, col + 1);
            
            if (size * size <= remainingArea && canPlaceSquare(row, col, size)) {
                markArea(row, col, size, currentCount + 1);
                printGrid();
                
                squares[currentCount].row = row;
                squares[currentCount].col = col;
                squares[currentCount].size = size;
                
                printf("Рекурсивный вызов с добавленным квадратом #%d (размер %d, позиция (%d, %d))\n", 
                       currentCount + 1, size, row + 1, col + 1);
                backtrack(currentCount + 1, squares, remainingArea - size * size);
                
                printf("Возврат из рекурсии, удаление квадрата из позиции (%d, %d) размера %d\n", 
                       row + 1, col + 1, size);
                markArea(row, col, size, 0);
                printGrid();
            } else {
                if (size * size > remainingArea) {
                    printf("  Квадрат слишком большой для оставшейся площади: %d > %d\n", 
                           size * size, remainingArea);
                }
            }
        }
    } else if (currentCount < minSquareCount) {
        saveSolution(currentCount, squares);
    }
}

void solve() {
    printf("\n=== Начало решения для N = %d ===\n", gridSize);
    
    optimalSolution = (SquareInfo*)malloc(gridSize * gridSize * sizeof(SquareInfo));
    SquareInfo* squares = (SquareInfo*)malloc(gridSize * gridSize * sizeof(SquareInfo));
    
    if (!handleSpecialCases()) {
        printf("\nПрименяем общий алгоритм для N = %d\n", gridSize);
        printf("Начальное размещение трех больших квадратов для разделения области\n");
        
        int maxWidth = (gridSize + 1) / 2;
        int largerWidth = gridSize - maxWidth;
        
        printf("Максимальная ширина: %d, Оставшаяся ширина: %d\n", maxWidth, largerWidth);
        
        squares[0].row = 0;
        squares[0].col = 0;
        squares[0].size = maxWidth;
        
        squares[1].row = 0;
        squares[1].col = maxWidth;
        squares[1].size = largerWidth;
        
        squares[2].row = maxWidth;
        squares[2].col = 0;
        squares[2].size = largerWidth;
        
        markArea(0, 0, maxWidth, 1);
        markArea(0, maxWidth, largerWidth, 2);
        markArea(maxWidth, 0, largerWidth, 3);
        
        printGrid();
        
        int remainingArea = gridSize * gridSize - maxWidth * maxWidth - 2 * largerWidth * largerWidth;
        printf("Размещены три начальных квадрата. Оставшаяся площадь: %d\n", remainingArea);
        
        backtrack(3, squares, remainingArea);
    }
    
    printf("\n=== ИТОГОВАЯ СТАТИСТИКА ===\n");
    printf("Всего вызовов backtrack: %d\n", backtrackCalls);
    printf("Размещено квадратов: %d\n", squaresPlaced);
    printf("Удалено квадратов: %d\n", squaresRemoved);
    
    printf("\n=== ФИНАЛЬНОЕ РЕШЕНИЕ ===\n");
    printf("%d\n", minSquareCount);
    for (int i = 0; i < minSquareCount; i++) {
        printf("%d %d %d\n", optimalSolution[i].row, optimalSolution[i].col, optimalSolution[i].size);
    }
    
    for (int i = 0; i < gridSize; i++) {
        for (int j = 0; j < gridSize; j++) {
            grid[i][j] = 0;
        }
    }
    
    for (int i = 0; i < minSquareCount; i++) {
        int row = optimalSolution[i].row - 1;
        int col = optimalSolution[i].col - 1;
        int size = optimalSolution[i].size;
        markArea(row, col, size, i + 1);
    }
    
    printf("\nФинальное расположение квадратов:\n");
    printGrid();
    
    free(squares);
    free(optimalSolution);
    
    for (int i = 0; i < gridSize; i++) {
        free(grid[i]);
    }
    free(grid);
}

int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 2 || n > 40) {
        printf("Ошибка: N должно быть в диапазоне [2, 40]\n");
        return 1;
    }
    
    gridSize = n;
    minSquareCount = gridSize * gridSize;
    
    printf("Задача о разбиении квадрата %d×%d на минимальное количество квадратов\n", n, n);
    
    grid = (int**)malloc(gridSize * sizeof(int*));
    for (int i = 0; i < gridSize; i++) {
        grid[i] = (int*)calloc(gridSize, sizeof(int));
    }
    
    solve();
    
    return 0;
}