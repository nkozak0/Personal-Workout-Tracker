import SwiftUI

struct RestTimerView: View {
    let seconds: Int
    @Environment(\.dismiss) var dismiss
    @State private var remaining: Int
    @State private var timer: Timer?
    
    init(seconds: Int) {
        self.seconds = seconds
        _remaining = State(initialValue: seconds)
    }
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Rest")
                .font(.largeTitle)
            Text("\(remaining)")
                .font(.system(size: 72, weight: .bold, design: .rounded))
            Button("Cancel") { dismiss() }
        }
        .onAppear(perform: start)
        .onDisappear { timer?.invalidate() }
    }
    
    private func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { t in
            if remaining > 0 {
                remaining -= 1
            } else {
                t.invalidate()
                dismiss()
            }
        }
    }
}
