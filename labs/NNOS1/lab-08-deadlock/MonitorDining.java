/** Monitor-based dining philosophers (deadlock-free by construction).
 *
 * <p>A single monitor owns all forks. A philosopher may only pick up both
 * forks atomically inside {@code synchronized} take(); otherwise it
 * {@code wait()}s. No hold-and-wait is possible, so Coffman's circular-wait
 * condition can never arise.
 *
 * <p>Compile/run (needs a JDK; not verified on the Linux lab host):
 * <pre>
 *   javac MonitorDining.java && java MonitorDining
 * </pre>
 */
public class MonitorDining {
    static final int N = 5;

    /** Monitor: all methods synchronized on this object. */
    static class Table {
        private final boolean[] forkFree = new boolean[N];

        Table() {
            for (int i = 0; i < N; i++) forkFree[i] = true;
        }

        /** Atomically take both forks; wait while either is busy. */
        synchronized void take(int id) throws InterruptedException {
            int left = id, right = (id + 1) % N;
            while (!forkFree[left] || !forkFree[right]) wait();
            forkFree[left] = false;
            forkFree[right] = false;
        }

        /** Return both forks and wake up waiters. */
        synchronized void put(int id) {
            forkFree[id] = true;
            forkFree[(id + 1) % N] = true;
            notifyAll();
        }
    }

    static class Philosopher extends Thread {
        private final int id;
        private final Table table;

        Philosopher(int id, Table table) {
            this.id = id;
            this.table = table;
        }

        @Override
        public void run() {
            try {
                for (int meal = 0; meal < 3; meal++) {
                    Thread.sleep(10); // thinking
                    table.take(id);
                    System.out.println("philosopher " + id + " eats (" + meal + ")");
                    Thread.sleep(10); // eating
                    table.put(id);
                }
                System.out.println("philosopher " + id + " done");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Table table = new Table();
        Philosopher[] ps = new Philosopher[N];
        for (int i = 0; i < N; i++) {
            ps[i] = new Philosopher(i, table);
            ps[i].start();
        }
        for (Philosopher p : ps) p.join(10000); // bounded: 10 s per thread
        boolean ok = true;
        for (Philosopher p : ps) {
            if (p.isAlive()) {
                System.out.println("FAIL: philosopher " + p.id + " still alive (deadlock?)");
                ok = false;
            }
        }
        System.out.println(ok ? "OK: all philosophers ate, no deadlock." : "FAIL");
    }
}
