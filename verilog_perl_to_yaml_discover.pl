#!/usr/bin/env perl
# Uses verilog-perls parser to spit out json (to import in python)
# Example Usage: verilog_perl_to_yaml.pl +incdir+../generated ../generated/fp16_add.sv

use warnings;
use strict;

use Verilog::Getopt;
use Verilog::Preproc;
 
package MyParser;

use Verilog::Netlist::File;
our @ISA = qw(Verilog::Netlist::File::Parser);


my @members;
my %structs;

my %ports = (
    input => [],
    output => [],
    );

# parse, parse_file, etc are inherited from Verilog::Parser
sub new {
     my $class = shift;
     # print "Class $class\n";
     my $self = $class->SUPER::new(@_);
     bless $self, $class;
     return $self;
}


sub yamlize {
    printf "-\n";
    foreach my $arg (@_) {
        if (!defined $arg) { # VerilogPerl is returning an unitialized variable
            $arg = "";
        }
        if ($arg =~ m/\"/) {
            printf "  - |\n    $arg\n";
        }
        else {
            printf "  - \"$arg\"\n" ;
        }
    }
}

# Override every callback method to dump yaml
sub create_yamlize {
    my $sub_name = shift;
    eval "sub $sub_name { my \$self = shift; yamlize(\$sub_name, \@_); \$self->SUPER::$sub_name(\@_); }";
}

# Ideally this would be generated
# Didn't spend much time look for a clever way
create_yamlize("attribute");
create_yamlize("class");
create_yamlize("contassign");
create_yamlize("covergroup");
create_yamlize("defparam");
create_yamlize("endcell");
create_yamlize("endclass");
create_yamlize("endgroup");
create_yamlize("endinterface");
create_yamlize("endmodport");
create_yamlize("endmodule");
create_yamlize("endpackage");
create_yamlize("endprogram");
create_yamlize("endtaskfunc");
create_yamlize("function");
create_yamlize("import");
create_yamlize("instant");
create_yamlize("interface");
create_yamlize("modport");
create_yamlize("module");
create_yamlize("package");
create_yamlize("parampin");
create_yamlize("pin");
create_yamlize("pinselects");
create_yamlize("port");
create_yamlize("program");
create_yamlize("task");
create_yamlize("var");

package main;
use Verilog::Netlist;

my $opt = new Verilog::Getopt;
@ARGV = $opt->parameter(@ARGV);

printf "---\n";

my $nl = new Verilog::Netlist(options => $opt, parser => "MyParser",);

while (my $filename = shift(@ARGV)) {
    $nl->read_file(filename=>$filename);
}
# Read in any sub-modules
$nl->link();
$nl->exit_if_error();
