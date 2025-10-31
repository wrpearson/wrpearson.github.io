#!/usr/bin/perl -Tw

use strict;

$ENV{PATH}="/usr/bin:/bin";

# use CGI::Carp qw(fatalsToBrowser carpout warningsToBrowser);
use CGI qw(header param start_html end_html);

use lib qw(/home/wrp/perllib/lib/site_perl /home/wrp/perllib/lib);
use HTML::Template;

sub BEGIN {
#  open(LOG, ">> /home/wrp/tmp/logs/errors.log") or die $!;
#  carpout(\*LOG);
}

use vars qw( $lect_line $date_line @lect_fields);

open(DATES,"dates18.list") || die "Cannot open dates18.list";
my @date_lines = <DATES>;
close(DATES);
@date_lines = grep {!/^#/} @date_lines;
chomp(@date_lines);

my $q = new CGI;

unless (!$q->param("lects_list") || -e 'lects18.list' ) {
    print $q->header();
    print $q->start_html("Error");
    print $q->h2("Lecture file not found");
    print $q->param();
    print $q->end_html();
    exit(1);
}

my $lfh;

if ($q->param("lects_list")) {
    unless ($lfh = $q->upload('lects_list')) {
	die "Could not open ".$q->param('lects_list');
    }
}
else {
    open ($lfh, "lects18.list") || die "cannot open lects18.list";
}

my @lect_lines;

{
  $/ = "\n>";
   @lect_lines = <$lfh>;
  chomp @lect_lines;
}

# remove first ^>
$lect_lines[0] =~ s/^>//;

my @lect_loop = ();

#if ($#lect_lines != $#date_lines ) {
#  die " record count mismatch: lectures: $#lect_lines != dates $#date_lines\n"
#}

my $tmpl = new HTML::Template(filename => './biol4230.tmpl',
			     die_on_bad_params => 0);

my $no_push = 0;
while ( @date_lines ) {
  $date_line = shift @date_lines;
  chomp($date_line);

  my %lect_row;

  @lect_row{"DAY","DATE","SPECIAL"} = split(/\t/,$date_line);

  if ($lect_row{"DAY"} =~ m/Tu/) {
    $lect_row{NEW_WEEK} = 1;
  } else {
    $lect_row{NEW_WEEK} = 0;
  }

  unless ($lect_row{'SPECIAL'} ) {
    $lect_line = shift @lect_lines;
    next unless $lect_line;


    @lect_fields = split("\n",$lect_line);
    chomp(@lect_fields);

    $lect_row{"TITLE"} = shift @lect_fields;
    while (@lect_fields) {
      my $lect_field = shift @lect_fields;
      next unless $lect_field;

      if ($lect_field =~ m/^\+/) {
	  push(@lect_loop, \%lect_row);
	  my %lect_row_p = ();
	  @lect_row_p{("DAY","DATE","NEW_WEEK","SPECIAL")} = ("","",0, 0);
	  $lect_row_p{"TITLE"} = substr($lect_field,1);
	  my $lect_field = shift(@lect_fields);
	  my ($tag, $value) = split('::', $lect_field );
	  $lect_row_p{$tag} = $value;
	  push(@lect_loop, \%lect_row_p);
	  $no_push = 1;
      }
      else {
	  my ($tag, $value) = split('::', $lect_field );
	  $lect_row{$tag} = $value;
	  $no_push = 0;
      }
    }
  } else {
    $lect_row{"TITLE"} = "<font color=red>" . $lect_row{"SPECIAL"} . "</font>";
  }
  push(@lect_loop,\%lect_row) unless ($no_push);
  $no_push = 0
}

$tmpl->param(LECT_LOOP=>\@lect_loop);

if ($ENV{DOCUMENT_ROOT}) {print header();}
print $tmpl->output();
