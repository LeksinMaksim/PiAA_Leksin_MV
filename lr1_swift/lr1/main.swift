import Foundation

class GridCoverSolver {
    private let empty = 0
    private typealias SquareInfo = (row: Int, col: Int, size: Int)
    private let gridSize: Int
    private var minSquareCount: Int
    private var optimalSolution: [SquareInfo]
    private var grid: [[Int]]
    
    init(gridSize: Int) {
        self.gridSize = gridSize
        self.minSquareCount = gridSize * gridSize
        self.optimalSolution = []
        self.grid = Array(repeating: Array(repeating: empty, count: gridSize), count: gridSize)
    }
    
    private func canPlaceSquare(atRow row: Int, col: Int, size: Int) -> Bool {
        guard row + size <= gridSize, col + size <= gridSize else { return false }
        return (row..<row + size).allSatisfy { i in
            (col..<col + size).allSatisfy { j in
                grid[i][j] == empty
            }
        }
    }
    
    private func markArea(atRow row: Int, col: Int, size: Int, withValue value: Int) {
        for i in row..<row + size {
            for j in col..<col + size {
                grid[i][j] = value
            }
        }
    }
    
    private func saveSolution(count: Int, squares: [SquareInfo]) {
        minSquareCount = count
        optimalSolution = squares
    }
    
    private func findFirstEmptyCell() -> (row: Int, col: Int)? {
        for row in 0..<gridSize {
            for col in 0..<gridSize {
                if grid[row][col] == empty {
                    return (row, col)
                }
            }
        }
        return nil
    }
    
    private func handleSpecialCases() -> Bool {
        if gridSize.isMultiple(of: 2) {
            let half = gridSize / 2
            let squares: [SquareInfo] = [
                (1, 1, half),
                (half + 1, 1, half),
                (half + 1, half + 1, half),
                (1, half + 1, half)
            ]
            saveSolution(count: 4, squares: squares)
            return true
        } else if gridSize.isMultiple(of: 3) {
            let third = gridSize / 3
            let squares: [SquareInfo] = [
                (1, 1, 2 * third),
                (1, 2 * third + 1, third),
                (third + 1, 2 * third + 1, third),
                (2 * third + 1, 1, third),
                (2 * third + 1, third + 1, third),
                (2 * third + 1, 2 * third + 1, third)
            ]
            saveSolution(count: 6, squares: squares)
            return true
        } else if gridSize.isMultiple(of: 5) {
            let fifth = gridSize / 5
            let squares: [SquareInfo] = [
                (1, 1, 3 * fifth),
                (3 * fifth + 1, 2 * fifth + 1, 2 * fifth),
                (3 * fifth + 1, 1, 2 * fifth),
                (1, 3 * fifth, 2 * fifth),
                (2 * fifth + 1, 3 * fifth + 1, fifth),
                (2 * fifth + 1, 4 * fifth + 1, fifth),
                (3 * fifth + 1, 4 * fifth + 1, fifth),
                (4 * fifth + 1, 4 * fifth + 1, fifth)
            ]
            saveSolution(count: 8, squares: squares)
            return true
        }
        return false
    }
    
    private func backtrack(currentCount: Int, squares: [SquareInfo], remainingArea: Int) {
        guard currentCount < minSquareCount else { return }
        
        if let (row, col) = findFirstEmptyCell() {
            let maxSize = min(gridSize - row, gridSize - col, gridSize - (gridSize - 1) / 2)
            for size in (1...maxSize).reversed() where size * size <= remainingArea {
                if canPlaceSquare(atRow: row, col: col, size: size) {
                    markArea(atRow: row, col: col, size: size, withValue: currentCount + 1)
                    let newSquares = squares + [(row + 1, col + 1, size)]
                    backtrack(currentCount: currentCount + 1, squares: newSquares, remainingArea: remainingArea - size * size)
                    markArea(atRow: row, col: col, size: size, withValue: empty)
                }
            }
        } else if currentCount < minSquareCount {
            saveSolution(count: currentCount, squares: squares)
        }
    }
    
    func solve() {
        if !handleSpecialCases() {
            let maxWidth = (gridSize + 1) / 2
            let largerWidth = gridSize - maxWidth
            let initialSquares: [SquareInfo] = [
                (1, 1, maxWidth),
                (1, maxWidth + 1, largerWidth),
                (maxWidth + 1, 1, largerWidth)
            ]
            markArea(atRow: 0, col: 0, size: maxWidth, withValue: 1)
            markArea(atRow: 0, col: maxWidth, size: largerWidth, withValue: 2)
            markArea(atRow: maxWidth, col: 0, size: largerWidth, withValue: 3)
            let remainingArea = gridSize * gridSize - maxWidth * maxWidth - 2 * largerWidth * largerWidth
            backtrack(currentCount: 3, squares: initialSquares, remainingArea: remainingArea)
        }
        print(minSquareCount)
        optimalSolution.forEach{print("\($0.0) \($0.1) \($0.2)")}
    }
}

if let input = readLine(), let n = Int(input), (2...40).contains(n) {
    let solver = GridCoverSolver(gridSize: n)
    solver.solve()
} else {
    print("Ошибка: N должно быть в диапазоне [2, 40]")
}
