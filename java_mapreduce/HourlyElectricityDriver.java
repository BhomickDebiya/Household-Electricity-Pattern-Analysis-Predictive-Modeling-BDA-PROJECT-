import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * HourlyElectricityDriver - Main driver for Hadoop MapReduce electricity job.
 * Handles existing output directory safely and executes the job.
 */
public class HourlyElectricityDriver {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: HourlyElectricityDriver <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Path inputPath = new Path(args[0]);
        Path outputPath = new Path(args[1]);

        // Safely check and delete output directory if it already exists to allow reruns
        FileSystem fs = outputPath.getFileSystem(conf);
        if (fs.exists(outputPath)) {
            System.out.println("Output directory " + outputPath + " already exists. Removing for fresh rerun...");
            fs.delete(outputPath, true);
        }

        Job job = Job.getInstance(conf, "Household Hourly Electricity Aggregation");
        job.setJarByClass(HourlyElectricityDriver.class);
        job.setMapperClass(HourlyElectricityMapper.class);
        job.setReducerClass(HourlyElectricityReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(DoubleWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outputPath);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
