import java.io.IOException;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * HourlyElectricityReducer - Aggregates Global_active_power for each hour.
 * Computes average power consumption (kW) and record count.
 * Emits: (Hour, "AvgPower_kW\tTotalRecords")
 */
public class HourlyElectricityReducer extends Reducer<Text, DoubleWritable, Text, Text> {
    private Text result = new Text();

    @Override
    public void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
        double sum = 0.0;
        long count = 0;
        for (DoubleWritable val : values) {
            sum += val.get();
            count++;
        }
        if (count > 0) {
            double avg = sum / count;
            result.set(String.format("%.4f\t%d", avg, count));
            context.write(key, result);
        }
    }
}
