import SwiftUI

@main
struct PersonalWorkoutTrackerApp: App {
    @StateObject private var store = DataStore()
    
    var body: some Scene {
        WindowGroup {
            if store.userProfile == nil {
                SetupView()
                    .environmentObject(store)
            } else {
                TabView {
                    WorkoutView()
                        .environmentObject(store)
                        .tabItem {
                            Label("Workout", systemImage: "figure.strengthtraining.traditional")
                        }
                    ProgressViewScreen()
                        .environmentObject(store)
                        .tabItem {
                            Label("Progress", systemImage: "chart.line.uptrend.xyaxis")
                        }
                }
            }
        }
    }
}

final class DataStore: ObservableObject {
    @Published var userProfile: UserProfile? {
        didSet { saveProfile() }
    }
    @Published var workoutLogs: [WorkoutLog] = [] {
        didSet { saveLogs() }
    }
    
    private let profileKey = "userProfile"
    private let logsKey = "workoutLogs"
    
    init() {
        loadProfile()
        loadLogs()
    }
    
    func saveWorkoutDay(date: Date, exercises: [ExerciseLog]) {
        let log = WorkoutLog(date: date, exercises: exercises)
        workoutLogs.append(log)
    }
    
    // MARK: Persistence
    private func loadProfile() {
        guard
            let data = UserDefaults.standard.data(forKey: profileKey),
            let profile = try? JSONDecoder().decode(UserProfile.self, from: data)
        else { return }
        userProfile = profile
    }
    private func saveProfile() {
        guard let profile = userProfile,
              let data = try? JSONEncoder().encode(profile) else { return }
        UserDefaults.standard.set(data, forKey: profileKey)
    }
    private func loadLogs() {
        guard
            let data = UserDefaults.standard.data(forKey: logsKey),
            let logs = try? JSONDecoder().decode([WorkoutLog].self, from: data)
        else { return }
        workoutLogs = logs
    }
    private func saveLogs() {
        guard let data = try? JSONEncoder().encode(workoutLogs) else { return }
        UserDefaults.standard.set(data, forKey: logsKey)
    }
}
