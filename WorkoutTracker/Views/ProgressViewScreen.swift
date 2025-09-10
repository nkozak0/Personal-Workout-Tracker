import SwiftUI
import Charts

struct ProgressViewScreen: View {
    @EnvironmentObject var store: DataStore
    
    var body: some View {
        NavigationView {
            List {
                ForEach(exerciseNames, id: \.self) { name in
                    NavigationLink(name) {
                        ExerciseProgressView(exerciseName: name)
                            .environmentObject(store)
                    }
                }
            }
            .navigationTitle("Progress")
        }
    }
    
    private var exerciseNames: [String] {
        Set(store.workoutLogs.flatMap { $0.exercises.map { $0.name } }).sorted()
    }
}

struct ExerciseProgressView: View {
    let exerciseName: String
    @EnvironmentObject var store: DataStore
    
    var body: some View {
        Chart(entries) { entry in
            LineMark(
                x: .value("Date", entry.date),
                y: .value("Weight", entry.maxWeight)
            )
            PointMark(
                x: .value("Date", entry.date),
                y: .value("Weight", entry.maxWeight)
            )
            .foregroundStyle(entry.color)
        }
        .padding()
        .navigationTitle(exerciseName)
    }
    
    private var entries: [ProgressEntry] {
        store.workoutLogs.compactMap { log in
            guard let exercise = log.exercises.first(where: { $0.name == exerciseName }) else { return nil }
            let maxWeight = exercise.setLogs.map(\.$weight).max() ?? 0
            let avgReps = exercise.setLogs.map(\.$reps).reduce(0, +) / max(1, exercise.setLogs.count)
            let diff = abs(avgReps - exercise.targetReps)
            let color: Color = diff >= 5 ? .red : (diff >= 2 ? .yellow : .green)
            return ProgressEntry(date: log.date, maxWeight: maxWeight, color: color)
        }
    }
}

struct ProgressEntry: Identifiable {
    let id = UUID()
    let date: Date
    let maxWeight: Double
    let color: Color
}
