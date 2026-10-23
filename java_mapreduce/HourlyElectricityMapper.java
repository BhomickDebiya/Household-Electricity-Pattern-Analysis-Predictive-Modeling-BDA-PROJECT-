import java.io.IOException;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * HourlyElectricityMapper - Extracts hour and Global_active_power from electricity records.
 * Input format: Date;Time;Global_active_power;...
 * Emits: (Text(Hour), DoubleWritable(Global_active_power))
 */
public class HourlyElectricityMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {
    private Text hourKey = new Text();
    private DoubleWritable powerVal = new DoubleWritable();

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString().trim();
        // Skip header or empty line
        if (line.isEmpty() || line.startsWith("Date")) {
            return;
        }
        String[] tokens = line.split(";");
        if (tokens.length >= 3) {
            String timeStr = tokens[1].trim();
            String powerStr = tokens[2].trim();
            // Handle UCI dataset missing value notation '?'
            if (powerStr.equals("?") || powerStr.isEmpty()) {
                return;
            }
            try {
                String[] timeParts = timeStr.split(":");
                String hour = timeParts[0];
                double power = Double.parseDouble(powerStr);
                hourKey.set(hour);
                powerVal.set(power);
                context.write(hourKey, powerVal);
            } catch (Exception e) {
                // Ignore malformed rows safely
            }
        }
    }
}
