import Foundation

struct UserProfile: Codable {
    var name: String
    var weight: Double
    var restSeconds: Int
    var schedule: [Weekday: [ExercisePlan]]
}

enum Weekday: String, Codable, CaseIterable, Identifiable {
    case sunday, monday, tuesday, wednesday, thursday, friday, saturday
    var id: String { rawValue }
    var display: String { rawValue.capitalized }
}

struct ExercisePlan: Codable, Identifiable {
    var id = UUID()
    var name: String
    var sets: Int
    var targetReps: Int
}
