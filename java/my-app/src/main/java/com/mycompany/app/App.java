package com.mycompany.app;
// import edu.lps.acs.ml.ngram3.NGramGeneric;

// /**
//  * Hello world!
//  *
//  */
// public class App 
// {
//     public static void main( String[] args )
//     {
//         NGramGeneric ngram = new NGramGeneric();
//         System.out.println( "Hello World!" );
//     }
// }
import edu.lps.acs.ml.ngram3.NGramGeneric;
import edu.lps.acs.ml.ngram3.alphabet.AlphabetGram;
import edu.lps.acs.ml.ngram3.utils.FileConverter;
import edu.lps.acs.ml.ngram3.utils.GZIPHelper;
import edu.lps.acs.ml.autoyara.SigCandidate;
import edu.lps.acs.ml.autoyara.CountingBloom;
import edu.lps.acs.ml.autoyara.AutoYaraCluster;
import java.nio.file.Path;
import java.io.BufferedInputStream;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.nio.file.FileVisitOption;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.OpenOption;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.SortedSet;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.stream.BaseStream;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;


import py4j.GatewayServer;

public class App {

  // public int addition(int first, int second) {
  //   return first + second;
  // }
  int test_val = 3;
  static public List<Path> getAllChildrenFiles(Path... sourceDirs)
  {   
    return getAllChildrenFiles(Arrays.asList(sourceDirs).stream().map(f->f.toFile()).collect(Collectors.toList()));
  }           
     
  static public List<Path> getAllChildrenFiles(File... sourceDirs)
  {                                  
    return getAllChildrenFiles(Arrays.asList(sourceDirs));
  }       
        
  static public List<Path> getAllChildrenFiles(List<File> sourceDirs)
  {           
            
            
    List<Path> targets = sourceDirs.stream().flatMap(f->
    {
        try 
        {   
            return Files.walk(f.toPath(), FileVisitOption.FOLLOW_LINKS).filter(Files::isRegularFile);
        }
        catch (IOException ex)
        {   
            Logger.getLogger(App.class.getName()).log(Level.SEVERE, null, ex);
            return new ArrayList<Path>().stream();
        }   
    }).collect(Collectors.toList());
    return targets;
  }  
  static public <T, S extends BaseStream<T, S>> Stream<T> wrap(Stream<T> stream, String task, boolean silent)
  {
      return stream;
      // if(silent)
      //     return stream;
      // else
      //     return ProgressBar.wrap(stream, task);
  } 

  public static List<SigCandidate> myBuildCandidateSet(String inDir, String benBloomDir, String malBloomDir, int gram_size, int toKeep, long max_filter_size, boolean silent, double fp_rate){
    // int gram_size = 256;
    // int toKeep = 100;
    
    // long max_filter_size = 100;
    // boolean silent = false;
    // double fp_rate = 0.001;


    File dir = new File(inDir);
    File ben_bloom_dir = new File(benBloomDir);
    File mal_bloom_dir = new File(malBloomDir);
    Map<Integer, CountingBloom> ben_blooms = null;
    Map<Integer, CountingBloom> mal_blooms = null;
    try{
      ben_blooms = collectBloomFilters(ben_bloom_dir);
      mal_blooms = collectBloomFilters(mal_bloom_dir);
    }
    catch (IOException ex)
    {
        Logger.getLogger(AutoYaraCluster.class.getName()).log(Level.SEVERE, null, ex);
    }
    
    List<Path> targets = getAllChildrenFiles(dir);

    List<SigCandidate> final_candidates = AutoYaraCluster.buildCandidateSet(targets, gram_size, ben_blooms, mal_blooms, max_filter_size, toKeep, silent, fp_rate);
    System.out.println(final_candidates.size());
    return final_candidates;

  }

  //public static Map<AlphabetGram, AtomicInteger> getNGrams(String inDir, String benBloomDir, String malBloomDir){
  //  int gram_size = 256;
  //  int toKeep = 100;
  //  long max_filter_size = 100;
  //  boolean silent = false;
  //  double fp_rate = 0.001;


  //  File dir = new File(inDir);
  //  File ben_bloom_dir = new File(benBloomDir);
  //  File mal_bloom_dir = new File(malBloomDir);

  //  Map<Integer, CountingBloom> ben_blooms = collectBloomFilters(ben_bloom_dir);
  //  Map<Integer, CountingBloom> mal_blooms = collectBloomFilters(mal_bloom_dir);
    

    
  //  List<Path> targets = getAllChildrenFiles(dir);
  //  long totalbytes = targets.stream().mapToLong(p->
  //  {
  //    try
  //    {
  //        return Files.size(p);
  //    }
  //    catch (IOException ex)
  //    {
  //        Logger.getLogger(App.class.getName()).log(Level.SEVERE, null, ex);
  //        return 0L;
  //    }
  //  }).sum();

  //  NGramGeneric ngram = new NGramGeneric();
  //  ngram.setAlphabetSize(256);
  //  long filter_size = Math.min(totalbytes/4, max_filter_size);
  //  ngram.setFilterSize((int) filter_size);
  //  ngram.setGramSize(gram_size);
  //  ngram.setTooKeep(toKeep);

  //  ngram.init();
  //  wrap(targets.parallelStream(), "Finding candidate " + gram_size  +"-byte sequences", silent)
  //      .forEach(p->
  //      {   
  //          try(InputStream in = new BufferedInputStream(GZIPHelper.getStream(Files.newInputStream(p))))
  //          {   
  //              ngram.hashCount(in);
  //          }   
  //          catch (IOException | InterruptedException ex) 
  //          {   
  //              Logger.getLogger(App.class.getName()).log(Level.SEVERE, null, ex);
  //          }   
  //      }); 


  //  ngram.finishHashCount();

  //  wrap(targets.parallelStream(), "Finding final " + gram_size  +"-byte sequences", silent)
  //      .forEach(p->
  //      {   
  //          try(InputStream in = new BufferedInputStream(GZIPHelper.getStream(Files.newInputStream(p))))
  //          {   
  //              ngram.exactCount(in);
  //          }   
  //          catch (IOException ex) 
  //          {
  //              Logger.getLogger(App.class.getName()).log(Level.SEVERE, null, ex);
  //          }
  //      });

  //  Map<AlphabetGram, AtomicInteger> final_candidates = ngram.finishExactCount();
  //  // return final_candidates;
    
  //  CountingBloom ben_bloom = ben_blooms.get(gram_size);
  //  CountingBloom mal_bloom = mal_blooms.get(gram_size);
  //  //your FP rates are too high! Remove them!
  //  final_candidates.entrySet().removeIf(e->
  //  {
  //      AlphabetGram candidate =  e.getKey();
        
  //      int num_00_ff = 0;
  //      for(int i = 0; i < candidate.size(); i++)
  //          if(candidate.get(i) == 0x00 || candidate.get(i) == 0xFF)
  //              num_00_ff++;
  //      if(num_00_ff > candidate.size()/2)
  //          return true;
        
  //      double ben_fp = ben_bloom.get(candidate) / (double) ben_bloom.divisor;
  //      double mal_fp = mal_bloom.get(candidate) / (double) mal_bloom.divisor;
  //      return ben_fp > fp_rate || mal_fp > fp_rate;
  //  });

  //  //Now we need to scan the data again. We have rough hit rates
  //  //but some of our input rules may be very corelated with eachother
  //  //so lets figure that out 

  //  Map<AlphabetGram, Set<Integer>> files_occred_in = new HashMap<>();
  //  final_candidates.keySet().forEach(k->files_occred_in.put(k, new ConcurrentSkipListSet()));

  //  AtomicInteger simpleID = new AtomicInteger();
  //  wrap(targets.parallelStream(), "Determining co-occurance of " + gram_size  +"-byte sequences", silent)
  //      .forEach(p->
  //      {
  //          try(InputStream in = new BufferedInputStream(GZIPHelper.getStream(Files.newInputStream(p))))
  //          {
  //              ngram.incrementConuts(in, simpleID.getAndIncrement(), files_occred_in);
  //          }
  //          catch (IOException ex)
  //          {
  //              Logger.getLogger(App.class.getName()).log(Level.SEVERE, null, ex);
  //          }
  //      });


  //  Map<SigCandidate, Set<Integer>> cur_working_set = new ConcurrentHashMap<>(files_occred_in.size());

  //  //Populate current working set to try and filter down. 
  //  files_occred_in.entrySet().parallelStream().forEach(e->
  //  {
  //      AlphabetGram candidate =  e.getKey();
  //      double ben_fp = ben_bloom.get(candidate) / (double) ben_bloom.divisor;
  //      double mal_fp = mal_bloom.get(candidate) / (double) mal_bloom.divisor;
  //      cur_working_set.put(new SigCandidate(candidate, ben_fp, mal_fp, e.getValue()), e.getValue());
  //  });


  //  List<SigCandidate> sigCandidates = Collections.EMPTY_LIST;
  //  sigCandidates = cur_working_set.keySet().parallelStream()
  //          .filter(s->s.getEntropy()>1.0)
  //          .collect(Collectors.toList());

  //  if(sigCandidates.isEmpty())//We need to try a different n-gram size
  //      return Collections.EMPTY_LIST;

  //  //Create a final candidate list, remove signatures that have 100% correlation with others
  //  List<SigCandidate> finalCandidates = new ArrayList<>();
  //  Map<Set<Integer>, List<SigCandidate>> coverageGrouped = new ConcurrentHashMap<>();
  //  //done i parallel b/c hashing cost on the Set<Integer> can be a bit pricy
  //  sigCandidates.parallelStream().forEach(s->
  //  {
  //      //slightly odd call structure ensures we don't fall victim to any race condition
  //      coverageGrouped.putIfAbsent(s.coverage, new ArrayList<>());
  //      List<SigCandidate> storage = coverageGrouped.get(s.coverage);
        
  //      //copute entropy now in parallel for use later
  //      synchronized(storage)
  //      {
  //          storage.add(s);
  //      }
  //  });
    
  //  for(List<SigCandidate> group : coverageGrouped.values())
  //  {
  //      //Pick gram with maximum entropy
  //      if(!group.isEmpty())
  //          finalCandidates.add(Collections.max(group, (SigCandidate arg0, SigCandidate arg1) -> Double.compare(arg0.getEntropy(), arg1.getEntropy())));
  //  }
    
  //  return finalCandidates;


  //}

  public static Map<Integer, CountingBloom>  collectBloomFilters(File bloom_dir) throws IOException
  {
      Map<Integer, CountingBloom> blooms = new HashMap<>();
      Files.walk(bloom_dir.toPath(), FileVisitOption.FOLLOW_LINKS)
              //just bloom filters
              .filter(p->p.getFileName().toString().endsWith(".bloom"))
              .forEach(p->
              {
                  try(ObjectInputStream ois = new ObjectInputStream(new BufferedInputStream(Files.newInputStream(p))))
                  {
                      CountingBloom bloom = (CountingBloom) ois.readObject();
                      int gram_size = bloomNameToGramSize(p.getFileName().toString());
                      blooms.put(gram_size, bloom);
                  }
                  catch (IOException | ClassNotFoundException ex)
                  {
                      Logger.getLogger(App.class.getName()).log(Level.SEVERE, null, ex);
                  }
              });
      return blooms;
  }
  public static int bloomNameToGramSize(String s) throws NumberFormatException
  {
      String[] tmp = s.replace(".bloom", "").split("_");
      return Integer.parseInt(tmp[tmp.length-1]);
  }

  public static void main(String[] args) {
    // NGramGeneric ngram = new NGramGeneric();
    App app = new App();
    // app is now the gateway.entry_point
    GatewayServer server = new GatewayServer(app);
    server.start();
    System.out.println("GatewayServer started");
  }
}

// public class RoughTest {
//   public static void main(String args[]){
//     NGramGeneric ngram = new NGramGeneric();
//     System.out.println("Hello World");
//     System.getProperty("java.classpath");
//   }

// }

