#!/usr/bin/perl
# ZooKeeper 
# Logfile Malware harvester
# v.0.2 

use LWP::Simple;
use URI::Find;	#EZMode
use Data::Dumper;
use strict;
use warnings;

if (@ARGV != 2){
	die "Usage: ZooKeeper.pl <log_file> <zoo_folder>\n";
}

#global URI
my $resource;
#folder number
my $i = 0;
my $finder = URI::Find->new(\&findCallBack);

sub findCallBack(){
	my $uri = shift;
	$resource = $uri;
}

sub handleResource($){
	my $log = shift;
	mkdir "$ARGV[1]$i";
	my $return_code = getstore($resource,"$ARGV[1]$i/file");
	print "[+] File download returned with: $return_code\n";
	open(LOG, ">>$ARGV[1]$i/log.txt") or warn "[!] Error: $! ";
	print LOG $log;
	close(LOG);
}

sub checkDupe($){
	my $string = shift;
	my $known = 0;
	open(KL,'+<', "./known_links") || die "[!] Error: $!";
	while (<KL>) {
   		$known = 1 if /\Q$string/;
	}
	#eof
	print KL "$string\n" if $known eq 0;
	close(KL);
	return $known;
}

### Main loop - continiously read file. 
open(FH,'<',$ARGV[0]) || die "[!] Error: $!";
print "[+] Zookeeper initiated\n";
for (;;){
	while(<FH>){
		$finder->find(\$_);
		my $log = $_;
		if($resource && checkDupe($resource) eq 0){
			print "[+] Resource found: $resource\n";
			handleResource($log);
			$resource = '';
			$i++;
		}
	}
	sleep 1;
	seek FH, 0, 1;
}
