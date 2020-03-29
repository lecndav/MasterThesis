package main

import (
	"context"
	"io"
	"io/ioutil"
	"os"
	"time"

	"abt-repo.de.bosch.com/go/can/canmeasured"

	"abt-repo.de.bosch.com/go/can"
	"abt-repo.de.bosch.com/go/measured"
	"github.com/sirupsen/logrus"
	"github.com/spf13/pflag"
	"gopkg.in/yaml.v2"
)

// Config stores a configuration for a gateway.
type Config struct {
	Name      string           `yaml:"Name"`
	DocsPath  string           `yaml:"Docspath"`
	Providers []ConfigProvider `yaml:"Providers"`
	Network   string           `yaml:"Network"`
	Address   string           `yaml:"Address"`
}

// Config stores a configuration for a gateway.
type ConfigProvider struct {
	Identifier string `yaml:"ID"`
	Source     string `yaml:"Source"`
	Name       string `yaml:"Name"`
	ConfigFile string `yaml:"Config"`
}

var (
	cfgFile = pflag.StringP("config", "c", "./config.yaml", "Path to the config file")
)

func main() {
	logger := logrus.New()
	logger.SetLevel(logrus.DebugLevel)

	if _, err := os.Stat("/media/myssddisk/ssdpresent.txt"); os.IsNotExist(err) {
		logger.Fatalf("SDD not mounted. Exit")
	}

	pflag.Parse()
	cfgFile, err := os.Open(*cfgFile)
	if err != nil {
		logger.Fatalf("Error opening config file: %+v", err)
	}

	cfg, err := ReadConfig(cfgFile)
	if err != nil {
		logger.Fatalf("Error opening config file: %+v", err)
	}

	mclient := measured.NewClient(cfg.Name, uint64(time.Now().UnixNano()), time.Nanosecond)
	mclient.DisableTimestampOffset()
	logger.Debugf("Netwotk: %s", cfg.Network)
	err = mclient.Dial(cfg.Network, cfg.Address)
	if err != nil {
		logger.Fatalf("%+v", err)
	}
	err = mclient.StartMeasurement()
	if err != nil {
		logger.Fatalf("%+v", err)
	}

	for _, providerCfg := range cfg.Providers {
		canPort, err := can.NewPort(providerCfg.Source)
		if err != nil {
			logger.Fatalf("%+v", err)
		}
		canLogger := canmeasured.NewCANLogger(canPort, mclient, providerCfg.Source, logger)
		err = canLogger.LoadConfigFile(providerCfg.ConfigFile)
		if err != nil {
			logger.Fatalf("%+v", err)
		}

		ctx, _ := context.WithCancel(context.Background())
		go canLogger.Read(ctx)
	}
	select {} // Read forever
}

// Reads in and parses a config
func ReadConfig(r io.Reader) (*Config, error) {
	raw, err := ioutil.ReadAll(r)
	if err != nil {
		return nil, err
	}
	c := &Config{}
	err = yaml.Unmarshal(raw, c)
	if err != nil {
		return nil, err
	}
	return c, err
}
