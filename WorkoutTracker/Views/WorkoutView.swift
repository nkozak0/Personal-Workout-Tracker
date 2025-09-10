import SwiftUI

struct WorkoutView: View {
    @EnvironmentObject var store: DataStore
    @State private var exerciseLogs: [ExerciseLog] = []
    @State private var showSummary = false
    
    private var todayPlan: [ExercisePlan] {
        guard let profile = store.userProfile else { return [] }
        let weekday = Weekday.allCases[Calendar.current.component(.weekday, from: Date()) - 1]
        return profile.schedule[weekday] ?? []
    }
    
    var body: some View {
        NavigationView {
            List {
                ForEach(exerciseLogs.indices, id: \.self) { idx in
                    ExerciseLogger(log: $exerciseLogs[idx], restSeconds: store.userProfile?.restSeconds ?? 60)
                }
            }
            .navigationTitle("Today's Workout")
            .toolbar {
                Button("Finish") { finishWorkout() }
            }
            .onAppear {
                if exerciseLogs.isEmpty {
                    exerciseLogs = todayPlan.map { plan in
                        ExerciseLog(name: plan.name, setLogs: Array(repeating: SetLog(weight: 0, reps: 0), count: plan.sets), targetReps: plan.targetReps)
                    }
                }
            }
            .sheet(isPresented: $showSummary) {
                WorkoutSummaryView(exercises: exerciseLogs)
                    .onDisappear { reset() }
            }
        }
    }
    
    private func finishWorkout() {
        store.saveWorkoutDay(date: Date(), exercises: exerciseLogs)
        showSummary = true
    }
    private func reset() {
        exerciseLogs.removeAll()
    }
}

struct ExerciseLogger: View {
    @Binding var log: ExerciseLog
    let restSeconds: Int
    @State private var currentSet = 0
    @State private var showTimer = false
    
    var body: some View {
        Section(header: Text(log.name)) {
            ForEach(log.setLogs.indices, id: \.self) { index in
                HStack {
                    Text("Set \(index + 1)")
                    Spacer()
                    TextField("Wt", value: $log.setLogs[index].weight, format: .number)
                        .keyboardType(.decimalPad)
                        .frame(width: 60)
                    TextField("Reps", value: $log.setLogs[index].reps, format: .number)
                        .keyboardType(.numberPad)
                        .frame(width: 50)
                }
            }
            Button("Start Rest Timer") {
                showTimer = true
            }
            .sheet(isPresented: $showTimer) {
                RestTimerView(seconds: restSeconds)
            }
        }
    }
}

struct WorkoutSummaryView: View {
    let exercises: [ExerciseLog]
    
    var body: some View {
        NavigationView {
            List {
                ForEach(exercises) { log in
                    VStack(alignment: .leading) {
                        Text(log.name).font(.headline)
                        ForEach(log.setLogs) { set in
                            Text("Wt: \(set.weight, specifier: "%.0f") lbs - Reps: \(set.reps)")
                        }
                    }
                }
            }
            .navigationTitle("Summary")
        }
    }
}
