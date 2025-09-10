import SwiftUI

struct SetupView: View {
    @EnvironmentObject var store: DataStore
    @State private var name: String = ""
    @State private var weight: String = ""
    @State private var restSeconds: String = "60"
    @State private var schedule: [Weekday: [ExercisePlan]] = [:]
    
    var body: some View {
        Form {
            Section(header: Text("Profile")) {
                TextField("Name", text: $name)
                TextField("Weight (lbs)", text: $weight)
                    .keyboardType(.decimalPad)
                TextField("Rest Seconds", text: $restSeconds)
                    .keyboardType(.numberPad)
            }
            Section(header: Text("Weekly Schedule")) {
                ForEach(Weekday.allCases) { day in
                    NavigationLink(day.display) {
                        ExerciseDayEditor(day: day, exercises: $schedule[day, default: []])
                    }
                }
            }
            Button("Save") { saveProfile() }
                .disabled(name.isEmpty || Double(weight) == nil)
        }
        .navigationTitle("Setup")
    }
    
    private func saveProfile() {
        guard let weightValue = Double(weight), let rest = Int(restSeconds) else { return }
        let profile = UserProfile(name: name, weight: weightValue, restSeconds: rest, schedule: schedule)
        store.userProfile = profile
    }
}

struct ExerciseDayEditor: View {
    let day: Weekday
    @Binding var exercises: [ExercisePlan]
    @State private var newName: String = ""
    @State private var sets: String = "3"
    @State private var reps: String = "12"
    
    var body: some View {
        Form {
            Section {
                TextField("Exercise Name", text: $newName)
                TextField("Sets", text: $sets).keyboardType(.numberPad)
                TextField("Target Reps", text: $reps).keyboardType(.numberPad)
                Button("Add") {
                    guard
                        !newName.isEmpty,
                        let setCount = Int(sets),
                        let repCount = Int(reps)
                    else { return }
                    exercises.append(ExercisePlan(name: newName, sets: setCount, targetReps: repCount))
                    newName = ""
                }
            }
            Section {
                ForEach(exercises) { exercise in
                    Text("\(exercise.name) - \(exercise.sets)x\(exercise.targetReps)")
                }
                .onDelete { index in
                    exercises.remove(atOffsets: index)
                }
            }
        }
        .navigationTitle(day.display)
    }
}
