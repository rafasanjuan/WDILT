-- phpMyAdmin SQL Dump

CREATE TABLE `users` (
  `username` varchar(30) NOT NULL,
  `password` varchar(60) NOT NULL
);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `username` (`username`);
COMMIT;
