import Foundation

struct WorkoutLog: Codable, Identifiable {
    var id = UUID()
    var date: Date
    var exercises: [ExerciseLog]
}

struct ExerciseLog: Codable, Identifiable {
    var id = UUID()
    var name: String
    var setLogs: [SetLog]
    var targetReps: Int
}

struct SetLog: Codable, Identifiable {
    var id = UUID()
    var weight: Double
    var reps: Int
}
